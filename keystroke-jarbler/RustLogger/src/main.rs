use aes_gcm::{Aes256Gcm, Key, Nonce}; // AES-GCM type aliases
use aes_gcm::aead::{Aead, KeyInit};
use aes_gcm::aead::generic_array::GenericArray;
use aes_gcm::aead::consts::U12;

use rand::RngCore;
use std::fs::OpenOptions;
use std::io::Write;
use std::env;

/// Define 96-bit AES-GCM Nonce type
type AesNonce = GenericArray<u8, U12>;

/// Load or generate a 256-bit AES key and return it
fn get_or_create_key() -> Result<Key<Aes256Gcm>, Box<dyn std::error::Error>> {
    let key_path = "aes_rust.key";
    if let Ok(bytes) = std::fs::read(key_path) {
        let key = Key::<Aes256Gcm>::from_slice(&bytes);
        return Ok(*key);
    }

    // Generate a secure new key
    let mut raw_key = [0u8; 32];
    rand::thread_rng().fill_bytes(&mut raw_key);
    std::fs::write(key_path, &raw_key)?;
    println!("[+] New AES key generated and saved.");
    Ok(*Key::<Aes256Gcm>::from_slice(&raw_key))
}

/// Generate a secure random 96-bit nonce
use aes_gcm::aead::generic_array::GenericArray;
type AesNonce = GenericArray<u8, typenum::U12>; // GCM expects 96-bit (12 byte) nonce

fn generate_nonce() -> AesNonce {
    let nonce_bytes = rand::random::<[u8; 12]>();
    GenericArray::from_slice(&nonce_bytes).clone()
}
/// Encrypt a message and write nonce+ciphertext to secure.log
fn encrypt_and_log(message: &str) -> Result<(), Box<dyn std::error::Error>> {
    let key = get_or_create_key()?;
    let cipher = Aes256Gcm::new(&key);
    let nonce = generate_nonce();

    let ciphertext = cipher
        .encrypt(&nonce, message.as_bytes())
        .map_err(|_| "Encryption failed")?;

    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open("secure.log")?;

    writeln!(file, "{}:{}", hex::encode(nonce), hex::encode(ciphertext))?;
    Ok(())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rust_logger \"message to log\"");
        return;
    }

    let message = &args[1];
    match encrypt_and_log(message) {
        Ok(_) => println!("[+] Encrypted log written."),
        Err(e) => eprintln!("[-] Logging failed: {}", e),
    }
}
