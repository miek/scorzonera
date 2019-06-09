extern crate byteorder;

use byteorder::{NativeEndian, WriteBytesExt};
use std::collections::VecDeque;

const WIDTH: usize = 327;
const HEIGHT: usize = 240;
const FRAME_SIZE_PIXELS: usize = WIDTH*HEIGHT;
const FRAME_SIZE_BYTES: usize = FRAME_SIZE_PIXELS*2;

pub struct FrameBuilder {
    data: VecDeque<u8>,
    state: SyncState,
}

impl FrameBuilder {
    pub fn new() -> Self {
        FrameBuilder {
            data: VecDeque::new(),
            state: SyncState::None,
        }
    }

    pub fn handle_data(&mut self, data: &[u8]) -> () {
        self.data.extend(data);
    }

    fn find_frame_start(&mut self) -> bool {
        if self.state != SyncState::FrameStart {
            let mut pos: Option<usize> = None;
            for (p, d) in self.data.iter().enumerate() {
                match (d, &self.state) {
                    (0xff, SyncState::VSyncMSB(count)) => {
                        self.state = SyncState::VSyncLSB(*count);
                    },
                    (0xff, _) => {
                        self.state = SyncState::VSyncLSB(0);
                    },
                    (0x7f, SyncState::VSyncLSB(count)) => {
                        self.state = SyncState::VSyncMSB(*count+1);
                    },
                    (_, SyncState::VSyncMSB(count)) if *count > 4 => {
                        self.state = SyncState::FrameStart;
                        pos = Some(p-2);
                        break;
                    },
                    (_, _) => {
                        self.state = SyncState::None;
                    },
                }
                pos = Some(p+1);
            }
            if let Some(pos) = pos {
                self.data.drain(0..pos);
            }
        }
        self.state == SyncState::FrameStart
    }

    pub fn get_frame(&mut self) -> Option<Vec<u16>> {
        if self.find_frame_start() && self.data.len() >= FRAME_SIZE_BYTES {
            let mut frame: Vec<u16> = Vec::with_capacity(FRAME_SIZE_PIXELS);
            let mut drain = self.data.drain(0..FRAME_SIZE_BYTES);
            for _ in 0..FRAME_SIZE_PIXELS {
                let v1 = drain.next().unwrap() as u16;
                let v2 = drain.next().unwrap() as u16;
                frame.push(v1 | (v2 << 8));
            }
            self.state = SyncState::None;
            //println!("frame");
            Some(frame)
        } else {
            None
        }
    }
}

#[derive(Debug, PartialEq)]
enum SyncState {
    None,
    VSyncLSB(u8),
    VSyncMSB(u8),
    FrameStart,
}

#[cfg(test)]
mod tests {
    use super::*;

    fn load_header(data: &[u8]) -> FrameBuilder {
        let mut fb = FrameBuilder::new();
        fb.handle_data(data); 
        fb.find_frame_start();
        fb
    }

    #[test]
    fn test_header_found() {
        let fb = load_header(&[0xaa, 0xaa, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0xaa]); 
        assert_eq!(fb.state, SyncState::FrameStart);
        assert_eq!(fb.data, VecDeque::from(vec![0xaa]));
    }
    #[test]
    fn test_header_found2() {
        let fb = load_header(&[0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0xaa]); 
        assert_eq!(fb.state, SyncState::FrameStart);
        assert_eq!(fb.data, VecDeque::from(vec![0xaa]));
    }
    #[test]
    fn test_header_found3() {
        let fb = load_header(&[0x01, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0xaa]); 
        assert_eq!(fb.state, SyncState::FrameStart);
        assert_eq!(fb.data, VecDeque::from(vec![0xaa]));
    }

    #[test]
    fn test_header_not_found() {
        let fb = load_header(&[0xaa, 0xaa, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0xaa]); 
        assert_ne!(fb.state, SyncState::FrameStart);
        assert_eq!(fb.data, VecDeque::new());
    }
}
