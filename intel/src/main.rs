#![no_std]
#![no_main]
#![feature(llvm_asm)]
#![feature(never_type)]

use core::panic::PanicInfo;

// the embedded rust book has a premade crate to start with this proc attribute
// https://docs.rs/cortex-m-rt-macros/0.1.8/src/cortex_m_rt_macros/lib.rs.html#77-165
// boils down to:
//   quote!(
//        #[doc(hidden)]
//        #[export_name = "main"]
//        pub unsafe extern "C" fn #tramp_ident() {
//            #ident(
//                #(#resource_args),*
//            )
//        }
//
//        #f
//    )
//    .into()
//

// Which allows us to do:
// #[entry]
// fn main() -> ! {
// 	loop {
// 	}	
// }

// We instead will use _start
#[no_mangle]
#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
pub extern "C" fn _start() -> ! {
	// expand macro rustc -Zunstable-options --pretty=expanded src/main.rs
	unsafe {
        llvm_asm!(include_str!("test.asm"));
		loop {}
    }
}
//#[export_name = "main"]
//pub unsafe extern "C" fn main() -> ! {
//	loop {}
//}

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
	loop {}
}
