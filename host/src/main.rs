extern crate sdl2;

mod greatfet;

use greatfet::{GreatFET, GREATFET_TRANSFER_BUFFER_SIZE, GREATFET_TRANSFER_POOL_SIZE};
use sdl2::pixels::{Color, PixelFormatEnum};
use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use std::fs::File;
use std::io::prelude::*;
use std::time::Duration;
use std::collections::VecDeque;

const WIDTH: usize = 327;
const HEIGHT: usize = 245;

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

    let context = libusb::Context::new().unwrap();

    let greatfets: Vec<_> = context.devices().unwrap().iter().filter(greatfet::filter).collect();
    let gf = GreatFET::new(&greatfets[0]).unwrap();

    let mut buffers = vec![];

    let mut async_group = libusb::AsyncGroup::new(&context);
    let timeout = Duration::from_secs(1);

    for _ in 0..GREATFET_TRANSFER_POOL_SIZE {
        let mut buf = vec![0u8; GREATFET_TRANSFER_BUFFER_SIZE];
        let mut buf = buf.into_boxed_slice();
        buffers.push(buf);
    }
    for buf in &mut buffers {
        async_group.submit(libusb::Transfer::bulk(&gf.handle, 0x81, buf, timeout)).unwrap();
    }

    let mut data: VecDeque<u8> = VecDeque::new();

    gf.start_receive(timeout).unwrap();
    let mut file = File::create("log.bin").unwrap();
    let mut sync = SyncState::None;
    'running: loop {
        let mut transfer = async_group.wait_any().unwrap();
        for d in transfer.actual() {
            data.push_back(*d);
        }
        //file.write_all(transfer.actual()).unwrap();
        async_group.submit(transfer).unwrap();

        for event in event_pump.poll_iter() {
            match event {
                Event::Quit {..} |
                Event::KeyDown { keycode: Some(Keycode::Escape), .. } =>
                    break 'running,
                _ => (),
            };
        }

        while sync != SyncState::FrameStart {
            if let Some(a) = data.pop_front() {
                use SyncState::*;
                sync = match sync {
                    None => match a {
                        0x01 => VSyncLSB,
                        _ => None,
                    },
                    VSyncLSB => match a {
                        0x80 => VSyncMSB,
                        _ => None,
                    },
                    VSyncMSB => match a {
                        0x01 => VSyncLSB,
                        _ => {
                            data.push_front(a);
                            FrameStart
                        },
                    },
                    FrameStart => break
                }
            } else {
                break;
            }
        }

        if sync == SyncState::FrameStart && data.len() > (WIDTH*HEIGHT*2) {
            let mut drain = data.drain(0..WIDTH*HEIGHT*2);
            texture.with_lock(None, |buffer: &mut [u8], pitch: usize| {
                for y in 0..HEIGHT {
                    for x in 0..WIDTH {
                        let v1 = drain.next().unwrap() as u16;
                        let v2 = drain.next().unwrap() as u16;
                        let val: u16 = v1 | (v2 << 8); 
                        let val = ((val - 30000)) as u8;
                        let offset = y*pitch + x*3;
                        buffer[offset] = val;
                        buffer[offset+1] = val;
                        buffer[offset+2] = val;
                    }
                }
            }).unwrap();
            canvas.copy(&texture, None, None).unwrap();
            canvas.present();
            sync = SyncState::None;
        }
    }
}

#[derive(PartialEq)]
enum SyncState {
    None,
    VSyncLSB,
    VSyncMSB,
    FrameStart,
}
