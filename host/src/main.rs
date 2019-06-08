mod greatfet;

use greatfet::{GreatFET, GREATFET_TRANSFER_BUFFER_SIZE, GREATFET_TRANSFER_POOL_SIZE};
use std::time::Duration;

fn main() {
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

    gf.start_receive(timeout).unwrap();
    loop {
        let mut transfer = async_group.wait_any().unwrap();
        println!("Read: {:?} {:?}", transfer.status(), transfer.actual());
        async_group.submit(transfer).unwrap();
    }
}
