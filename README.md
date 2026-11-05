This project is a GUI Based Application that encrypts and decrypts text & files using Python. 

It was chosen as a practical way to learn how passwords, keys, encryption, decryption, and a graphical interface work together in one program. 

The user enters a message or upload files and a password, then selects Encrypt Text or Decrypt Text. 

The result appears in a separate output area, where it can be copied or cleared. 

The application uses Tkinter for the interface and the cryptography library for the cryptographic operations. 

Before encryption, it creates a random 16-byte salt and uses PBKDF2-HMAC-SHA256 to derive a key from the password. 

Fernet uses that key to encrypt the message and verify the encrypted token when decryption is attempted. 

The salt is stored with the token so the same key can be derived later. 

The combined data is encoded with URL-safe Base64 so it can be shown in a text box.

The program depends on the user remembering the password. 
