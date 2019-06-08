extern crate byteorder;
extern crate libusb;

use byteorder::{NativeEndian, WriteBytesExt};
use libusb::{Direction, RequestType, Recipient};
use std::time::Duration;

const GREATFET_VID: u16 = 0x1d50;
const GREATFET_PID: u16 = 0x60e6;
const GREATFET_USB_INTERFACE: u16 = 0;

pub const GREATFET_TRANSFER_POOL_SIZE: usize = 32;
pub const GREATFET_TRANSFER_BUFFER_SIZE: usize = 262144;

const GREATFET_LIBGREAT_REQUEST_NUMBER: u8 = 0x65;
const GREATFET_LIBGREAT_VALUE_EXECUTE: u16 = 0;
const GREATFET_TAXI_CLASS: u32 = 0x199;
const GREATFET_TAXI_VERB_START: u32 = 0;


pub struct GreatFET<'a> {
    device: &'a libusb::Device<'a>,
    pub handle: libusb::DeviceHandle<'a>,
}

impl<'a> GreatFET<'a> {
    pub fn new(device: &'a libusb::Device) -> Result<Self, Error> {
        let handle = device.open()?;
        Ok(GreatFET{
            device: device,
            handle: handle,
        })
    }

    pub fn execute_command(&self, command: &[u8], response: &mut [u8], timeout: Duration) -> Result<(), Error> {
        let flags = 0u16;
        let request_type = libusb::request_type(
            Direction::Out,
            RequestType::Vendor,
            Recipient::Endpoint,
        );
        self.handle.write_control(
            request_type,
            GREATFET_LIBGREAT_REQUEST_NUMBER,
            GREATFET_LIBGREAT_VALUE_EXECUTE,
            flags,
            command,
            timeout
        )?;

        let request_type = libusb::request_type(
            Direction::In,
            RequestType::Vendor,
            Recipient::Endpoint,
        );
        self.handle.read_control(
            request_type,
            GREATFET_LIBGREAT_REQUEST_NUMBER,
            GREATFET_LIBGREAT_VALUE_EXECUTE,
            0,
            response,
            timeout
        )?;
        Ok(())
    }

    pub fn start_receive(&self, timeout: Duration) -> Result<(), Error> {
        let mut response = vec![];
        let mut command = vec![];
        command.write_u32::<NativeEndian>(GREATFET_TAXI_CLASS).unwrap();
        command.write_u32::<NativeEndian>(GREATFET_TAXI_VERB_START).unwrap();
        self.execute_command(&command, &mut response, timeout)?;
        Ok(())
    }
}

pub fn filter(device: &libusb::Device) -> bool {
    let desc = device.device_descriptor().unwrap();
    (desc.vendor_id() == GREATFET_VID && desc.product_id() == GREATFET_PID)
}

#[derive(Debug)]
pub enum Error {
    LibUsb(libusb::Error),
}

impl From<libusb::Error> for Error {
    fn from(error: libusb::Error) -> Self {
        Error::LibUsb(error)
    }
}
