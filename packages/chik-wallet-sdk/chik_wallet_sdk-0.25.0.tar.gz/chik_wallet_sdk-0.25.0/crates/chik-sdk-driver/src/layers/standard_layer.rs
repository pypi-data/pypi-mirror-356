use chik_bls::PublicKey;
use chik_protocol::Coin;
use chik_puzzle_types::standard::{StandardArgs, StandardSolution};
use chik_puzzles::P2_DELEGATED_PUZZLE_OR_HIDDEN_PUZZLE_HASH;
use chik_sdk_types::Conditions;
use klvm_traits::{klvm_quote, FromKlvm};
use klvm_utils::{ToTreeHash, TreeHash};
use klvmr::{Allocator, NodePtr};

use crate::{DriverError, Layer, Puzzle, Spend, SpendContext, SpendWithConditions};

/// This is the actual puzzle name for the [`StandardLayer`].
pub type P2DelegatedOrHiddenLayer = StandardLayer;

/// The standard [`Layer`] is used for most coins on the Chik blockchain. It allows a single key
/// to spend the coin by providing a delegated puzzle (for example to output [`Conditions`]).
///
/// There is also additional hidden puzzle functionality which can be encoded in the key.
/// To do this, you calculate a "synthetic key" from the original key and the hidden puzzle hash.
/// When spending the coin, you can reveal this hidden puzzle and provide the original key.
/// This functionality is seldom used in Chik, and usually the "default hidden puzzle" is used instead.
/// The default hidden puzzle is not spendable, so you can only spend XCK coins by signing with your key.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct StandardLayer {
    pub synthetic_key: PublicKey,
}

impl StandardLayer {
    pub fn new(synthetic_key: PublicKey) -> Self {
        Self { synthetic_key }
    }

    pub fn spend(
        &self,
        ctx: &mut SpendContext,
        coin: Coin,
        conditions: Conditions,
    ) -> Result<(), DriverError> {
        let spend = self.spend_with_conditions(ctx, conditions)?;
        ctx.spend(coin, spend)
    }

    pub fn delegated_inner_spend(
        &self,
        ctx: &mut SpendContext,
        spend: Spend,
    ) -> Result<Spend, DriverError> {
        self.construct_spend(
            ctx,
            StandardSolution {
                original_public_key: None,
                delegated_puzzle: spend.puzzle,
                solution: spend.solution,
            },
        )
    }
}

impl Layer for StandardLayer {
    type Solution = StandardSolution<NodePtr, NodePtr>;

    fn construct_puzzle(&self, ctx: &mut SpendContext) -> Result<NodePtr, DriverError> {
        ctx.curry(StandardArgs::new(self.synthetic_key))
    }

    fn construct_solution(
        &self,
        ctx: &mut SpendContext,
        solution: Self::Solution,
    ) -> Result<NodePtr, DriverError> {
        ctx.alloc(&solution)
    }

    fn parse_puzzle(allocator: &Allocator, puzzle: Puzzle) -> Result<Option<Self>, DriverError> {
        let Some(puzzle) = puzzle.as_curried() else {
            return Ok(None);
        };

        if puzzle.mod_hash != P2_DELEGATED_PUZZLE_OR_HIDDEN_PUZZLE_HASH.into() {
            return Ok(None);
        }

        let args = StandardArgs::from_klvm(allocator, puzzle.args)?;

        Ok(Some(Self {
            synthetic_key: args.synthetic_key,
        }))
    }

    fn parse_solution(
        allocator: &Allocator,
        solution: NodePtr,
    ) -> Result<Self::Solution, DriverError> {
        Ok(StandardSolution::from_klvm(allocator, solution)?)
    }
}

impl SpendWithConditions for StandardLayer {
    fn spend_with_conditions(
        &self,
        ctx: &mut SpendContext,
        conditions: Conditions,
    ) -> Result<Spend, DriverError> {
        let delegated_puzzle = ctx.alloc(&klvm_quote!(conditions))?;
        self.construct_spend(
            ctx,
            StandardSolution {
                original_public_key: None,
                delegated_puzzle,
                solution: NodePtr::NIL,
            },
        )
    }
}

impl ToTreeHash for StandardLayer {
    fn tree_hash(&self) -> TreeHash {
        StandardArgs::curry_tree_hash(self.synthetic_key)
    }
}

#[cfg(test)]
mod tests {
    use chik_puzzle_types::Memos;
    use chik_sdk_test::Simulator;

    use super::*;

    #[test]
    fn test_flash_loan() -> anyhow::Result<()> {
        let mut sim = Simulator::new();
        let ctx = &mut SpendContext::new();
        let alice = sim.bls(1);
        let p2 = StandardLayer::new(alice.pk);

        p2.spend(
            ctx,
            alice.coin,
            Conditions::new().create_coin(alice.puzzle_hash, u64::MAX, Memos::None),
        )?;

        p2.spend(
            ctx,
            Coin::new(alice.coin.coin_id(), alice.puzzle_hash, u64::MAX),
            Conditions::new().create_coin(alice.puzzle_hash, 1, Memos::None),
        )?;

        sim.spend_coins(ctx.take(), &[alice.sk])?;

        Ok(())
    }
}
