use std::io;

use chik_consensus::validation_error::ErrorCode;
use chik_sdk_signer::SignerError;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum SimulatorError {
    #[error("IO error: {0}")]
    Io(#[from] io::Error),

    #[error("Validation error: {0:?}")]
    Validation(ErrorCode),

    #[error("Signer error: {0}")]
    Signer(#[from] SignerError),

    #[error("Missing key")]
    MissingKey,
}
