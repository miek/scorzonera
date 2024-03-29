mod frame_builder;

use frame_builder::FrameBuilder;
use palette::{LinSrgb, Hsv, Gradient};
use scarlet::colormap::ListedColorMap;
use sdl2::pixels::PixelFormatEnum;
use sdl2::event::Event;
use sdl2::keyboard::Keycode;

use std::io::prelude::*;
use std::fs::File;
use std::time::{Duration, Instant};

use frame_builder::WIDTH as WIDTH;
use frame_builder::HEIGHT as HEIGHT;

const VID: u16 = 0x16d0;
const PID: u16 = 0x0f3b;
const TRANSFER_POOL_SIZE: usize = 32;
const TRANSFER_BUFFER_SIZE: usize = 1024*160;

fn main() {
    let sdl_context = sdl2::init().unwrap();
    let video_subsystem = sdl_context.video().unwrap();
    let window = video_subsystem.window("taxi", WIDTH as u32, HEIGHT as u32)
        .position_centered()
        .build()
        .unwrap();

    let mut canvas = window.into_canvas().build().unwrap();
    let texture_creator = canvas.texture_creator();
    let mut texture = texture_creator.create_texture_streaming(PixelFormatEnum::RGB24, WIDTH as u32, HEIGHT as u32).unwrap();
    canvas.clear();
    canvas.present();
    let mut event_pump = sdl_context.event_pump().unwrap();

    let usb_context = libusb::Context::new().unwrap();

    let devices: Vec<_> = usb_context.devices().unwrap().iter().filter(
        |dev| {
            let desc = dev.device_descriptor().unwrap();
            desc.vendor_id() == VID && desc.product_id() == PID
        }
    ).collect();
    if devices.len() == 0 {
        println!("Device not found");
        return;
    }
    let handle = devices[0].open().unwrap();

    let mut buffers = allocate_buffers(TRANSFER_POOL_SIZE);
    let mut async_group = libusb::AsyncGroup::new(&usb_context);
    let timeout = Duration::from_secs(1);

    for buf in &mut buffers {
        async_group.submit(libusb::Transfer::bulk(&handle, 0x81, buf, timeout)).unwrap();
    }

    let mut fb = FrameBuilder::new();
    let mut frame_count = 0;
    let mut last_instant = Instant::now();

    let mut base = 32300;
    let mut gain = 30f32;
    let gradients = [
        Gradient::new(vec![
            // black
            Hsv::from(LinSrgb::new(0.0, 0.0, 0.0)),
            // to white
            Hsv::from(LinSrgb::new(1.0, 1.0, 1.0))
        ]),
        convert_listedcolormap(&ListedColorMap::inferno()),
    ];
    let mut colormaps = gradients.iter().cycle();
    let mut colormap = colormaps.next().unwrap();
    let mut lut = build_lut(base, gain, &colormap);
    let mut file = File::create("log.bin").unwrap();
    let mut pause = false;
    'running: loop {
        // Handle SDL events
        for event in event_pump.poll_iter() {
            let mut rebuild_lut = false;
            match event {
                Event::Quit {..} |
                Event::KeyDown { keycode: Some(Keycode::Escape), .. } |
                Event::KeyDown { keycode: Some(Keycode::Q), .. } =>
                    break 'running,
                Event::KeyDown { keycode: Some(Keycode::Space), .. } => {
                    colormap = colormaps.next().unwrap();
                    rebuild_lut = true;
                },
                Event::KeyDown { keycode: Some(Keycode::P), .. } => {
                    pause = !pause;
                },
                _ => (),
            };

            let adj = match event {
                Event::KeyDown { keycode: Some(Keycode::W), ..} => Some((-50, 0f32)),
                Event::KeyDown { keycode: Some(Keycode::S), ..} => Some((50, 0f32)),
                Event::KeyDown { keycode: Some(Keycode::A), ..} => Some((0, -0.6f32)),
                Event::KeyDown { keycode: Some(Keycode::D), ..} => Some((0, 0.6f32)),
                _ => None,
            };
            if let Some(adj) = adj {
                base = (base as i32 + adj.0) as u16;
                gain += adj.1;
                rebuild_lut = true
            }

            if rebuild_lut {
                lut = build_lut(base, gain, &colormap);
            }
        }

        // Wait for a USB transfer & pass it to the frame builder
        let mut transfer = async_group.wait_any().unwrap();
        file.write_all(&transfer.actual()).unwrap();
        // Display a frame if there's one ready
        if let Some(f) = fb.get_frame(transfer.actual()) {
            texture.with_lock(None, |buffer: &mut [u8], pitch: usize| {
                for y in 0..HEIGHT {
                    for x in 0..WIDTH {
                        let input_offset = y*WIDTH+x;
                        let val = f[input_offset];
                        let val = lut[val as usize];
                        let offset = y*pitch + x*3;
                        buffer[offset] = val.0;
                        buffer[offset+1] = val.1;
                        buffer[offset+2] = val.2;
                    }
                }
            }).unwrap();
            if !pause {
                canvas.copy(&texture, None, None).unwrap();
            }
            canvas.present();
            frame_count += 1;
        }
        async_group.submit(transfer).unwrap();

        // Print FPS
        if last_instant.elapsed().as_secs() >= 2 {
            println!("fps: {}", frame_count as f32 / 2.0);
            last_instant = Instant::now();
            frame_count = 0;
        }
    }
}

fn allocate_buffers(count: usize) -> Vec<[u8; TRANSFER_BUFFER_SIZE]> {
    (0..count).map(|_| [0u8; TRANSFER_BUFFER_SIZE]).collect()
}

fn build_lut(base: u16, gain: f32, colormap: &Gradient<Hsv>) -> Vec<(u8, u8, u8)> {
    let lut_size = 65536;
    let mut lut: Vec<(u8, u8, u8)> = Vec::with_capacity(lut_size);
    for i in 0..lut_size {
        let val = i.saturating_sub(base as usize) as f32 * gain as f32 / 65536f32;
        let mapped = colormap.get(val);
        let rgb = LinSrgb::from(mapped);
        lut.push((
            (rgb.red * 255f32) as u8,
            (rgb.green * 255f32) as u8,
            (rgb.blue * 255f32) as u8,
        ));
    }
    lut
}

fn convert_listedcolormap(cm: &ListedColorMap) -> Gradient<Hsv> {
    let vals: Vec<_> = cm.vals.iter().map(
        |v| Hsv::from(
            LinSrgb::new(
                v[0] as f32,
                v[1] as f32,
                v[2] as f32
            )
        )
    ).collect();
    Gradient::new(vals)
}

