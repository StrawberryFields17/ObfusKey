using System;
using System.Security.Cryptography;

namespace ObfusKey.Utils
{
    /// <summary>
    /// Utility class for generating secure AES encryption keys.
    /// </summary>
    public static class KeyGenerator
    {
        /// <summary>
        /// Generates a secure 256-bit AES key and returns it as a Base64 string.
        /// This can be saved and used later for symmetric encryption/decryption.
        /// </summary>
        /// <returns>Base64-encoded AES-256 key</returns>
        public static string GenerateBase64AesKey()
        {
            // Allocate 32 bytes (256 bits) for AES key
            byte[] key = new byte[32];

            // Use a cryptographically secure random number generator
            using (var rng = RandomNumberGenerator.Create())
            {
                // Fill the key array with secure random bytes
                rng.GetBytes(key);
            }

            // Convert the raw byte key to a Base64-encoded string for easy saving/sharing
            return Convert.ToBase64String(key);
        }
    }
}
