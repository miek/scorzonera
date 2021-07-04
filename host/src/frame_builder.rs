extern crate byteorder;

use std::io::Cursor;
use byteorder::{LittleEndian, ReadBytesExt};

pub const WIDTH: usize = 327;
pub const HEIGHT: usize = 245;
const FRAME_SIZE_PIXELS: usize = WIDTH*HEIGHT;

pub struct FrameBuilder {
}

impl FrameBuilder {
    pub fn new() -> Self {
        FrameBuilder {
        }
    }

    pub fn get_frame(&mut self, data: &[u8]) -> Option<Vec<u16>> {
        let mut frame: Vec<u16> = Vec::with_capacity(WIDTH*HEIGHT);
        let mut rdr = Cursor::new(data);
        while let Ok(pixel) = rdr.read_u16::<LittleEndian>() {
            frame.push(pixel);
        }
        if frame.len() < FRAME_SIZE_PIXELS {
            return None;
        }
        return Some(frame);
    }
}