mod announcements;
mod error;
mod key_pairs;
mod simulator;
mod transaction;

pub use announcements::*;
pub use error::*;
pub use key_pairs::*;
pub use simulator::*;
pub use transaction::*;

#[cfg(feature = "peer-simulator")]
mod peer_simulator;

#[cfg(feature = "peer-simulator")]
pub use peer_simulator::*;

use chik_protocol::{Bytes32, Program};
use klvm_traits::{FromKlvm, ToKlvm};
use klvm_utils::tree_hash;
use klvmr::Allocator;

pub fn to_program(value: impl ToKlvm<Allocator>) -> anyhow::Result<Program> {
    let mut allocator = Allocator::new();
    let ptr = value.to_klvm(&mut allocator)?;
    Ok(Program::from_klvm(&allocator, ptr)?)
}

pub fn to_puzzle(value: impl ToKlvm<Allocator>) -> anyhow::Result<(Bytes32, Program)> {
    let mut allocator = Allocator::new();
    let ptr = value.to_klvm(&mut allocator)?;
    let puzzle_reveal = Program::from_klvm(&allocator, ptr)?;
    let puzzle_hash = tree_hash(&allocator, ptr);
    Ok((puzzle_hash.into(), puzzle_reveal))
}

pub fn expect_spend<T>(result: Result<T, SimulatorError>, to_pass: bool) {
    if let Err(error) = result {
        assert!(!to_pass, "Expected spend to pass, but got {error}");
    } else if !to_pass {
        panic!("Expected spend to fail");
    }
}
