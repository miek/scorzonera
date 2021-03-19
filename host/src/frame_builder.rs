extern crate byteorder;

use std::io::Cursor;
use byteorder::{LittleEndian, ReadBytesExt};

pub const WIDTH: usize = 327;
pub const HEIGHT: usize = 245;
const FRAME_SIZE_PIXELS: usize = WIDTH*HEIGHT;

pub struct FrameBuilder {
    data: Vec<u8>,
    framebuffer: Vec<u16>,
    row: usize,
    column: usize,
}

impl FrameBuilder {
    pub fn new() -> Self {
        FrameBuilder {
            data: Vec::new(),
            framebuffer: vec![0; FRAME_SIZE_PIXELS],
            row: 0,
            column: 0,
        }
    }

    pub fn handle_data(&mut self, data: &[u8]) -> () {
        self.data.extend(data);
    }

    pub fn get_frame(&mut self) -> Option<Vec<u16>> {
        let mut rdr = Cursor::new(&self.data);
        while let Ok(data) = rdr.read_u16::<LittleEndian>() {
            match data {
                // hsync
                0x0001 => {
                    self.row += 1;
                    self.column = 0;
                    continue;
                },
                // vsync
                0x0000 => {
                    self.row = 0;
                    self.column = 0;
                    self.data.drain(0..rdr.position() as usize);
                    let fb = self.framebuffer.clone();
                    self.framebuffer = vec![65535; FRAME_SIZE_PIXELS];
                    return Some(fb);
                },
                // pixel
                x => {
                    if self.column >= WIDTH || self.row >= HEIGHT {
                        continue;
                    }
                    self.framebuffer[self.row*WIDTH + self.column] = x;
                    self.column += 1;
                },

            }
        }
        self.data.clear();
        return None;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

}
