---
title: "Mobile Application Security Guide"
description: "Mobile app security covering OWASP Mobile Top 10, code obfuscation, certificate pinning, secure storage, and runtime protection."
date: 2026-03-04
board: security
url: https://dingjiu1989-hue.github.io/en/security/mobile-security.html
---

# Mobile Application Security Guide

Mobile applications handle sensitive data and run in untrusted environments. Users download apps from various sources, connect to public Wi-Fi, and often jailbreak or root their devices. This guide covers the key security practices for mobile application development, based on the OWASP Mobile Top 10 and industry best practices.

## OWASP Mobile Top 10

The OWASP Mobile Top 10 is the authoritative list of mobile security risks. Understanding these risks is the first step toward mitigating them.

  * **Improper Platform Usage** : Misuse of mobile platform features, such as intents, custom URL schemes, or fingerprint APIs.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Insecure Data Storage** : Storing sensitive data in shared preferences, SQLite databases without encryption, or external storage.

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Insecure Communication** : Transmitting data over unencrypted channels or accepting invalid TLS certificates.

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Insecure Authentication** : Weak authentication mechanisms, missing session management, or hardcoded credentials.

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Insufficient Cryptography** : Using weak algorithms, hardcoded encryption keys, or improper random number generation.

6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Insecure Authorization** : Insecure direct object references and privilege escalation through client-side manipulation.

7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Client Code Quality** : Buffer overflows, memory leaks, and other code quality issues leading to security vulnerabilities.

8\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Code Tampering** : Binary patching, resource modification, and method swizzling.

9\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Reverse Engineering** : Decompilation and analysis of application code.

10\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Extraneous Functionality** : Hidden backdoors, debug endpoints, or test code left in production builds.

## Code Obfuscation

Mobile apps are distributed as binaries that run on user devices. Without protection, attackers can decompile the app and analyze its logic.

## Android Obfuscation with ProGuard / R8

ProGuard and R8 shrink, optimize, and obfuscate Android bytecode. They rename classes, methods, and fields to meaningless names and remove unused code.

// build.gradle (app level)

android {

buildTypes {

release {

minifyEnabled true

shrinkResources true

proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'),

'proguard-rules.pro'

}

}

}

## proguard-rules.pro

## Keep model classes used by Gson serialization

-keep class com.example.app.model.*_{_ ; }

## Keep logging in debug but strip in release

-assumenosideeffects class android.util.Log {

public static boolean isLoggable(java.lang.String, int);

public static int v(...);

public static int d(...);

}

## iOS Obfuscation

iOS apps are harder to reverse engineer than Android APKs due to the compiled ARM binary, but they are not immune. Use these techniques:

  * Strip debug symbols with the `strip` command during build.

  * Enable compiler optimizations (`-O2` or `-Os`).

  * Use LLVM obfuscator passes or commercial tools like iXGuard.

  * Encrypt string literals at compile time.




// String encryption helper

struct ObfuscatedString {

private let encrypted: [UInt8]

private let key: UInt8

func decrypt() -> String {

return String(bytes: encrypted.map { $0 ^ key }, encoding: .utf8) ?? ""

}

}

// Usage

let apiKey = ObfuscatedString(

encrypted: [0x34, 0x56, 0x78], // XOR-encoded

key: 0xAB

).decrypt()

## Certificate Pinning

Mobile apps must protect against man-in-the-middle (MITM) attacks, even when the device trusts a rogue CA due to malware or user action.

## What Certificate Pinning Does

Certificate pinning hardcodes the expected server certificate or public key in the app. The app rejects any connection where the server presents a different certificate, even if it chains to a trusted root CA.

## Implementation

**Android (OkHttp)** :

// Certificate pinning with OkHttp

val certificatePinner = CertificatePinner.Builder()

.add("api.example.com",

"sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")

.build()

val client = OkHttpClient.Builder()

.certificatePinner(certificatePinner)

.build()

**iOS (URLSession)** :

// Certificate pinning in URLSession delegate

func urlSession(_ session: URLSession,

didReceive challenge: URLAuthenticationChallenge,

completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {

guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,

let serverTrust = challenge.protectionSpace.serverTrust else {

completionHandler(.performDefaultHandling, nil)

return

}

// Compare server certificate with pinned certificate

let pinnedCertData = pinnedCertificateData()

if let serverCert = SecTrustGetCertificateAtIndex(serverTrust, 0) {

let serverCertData = SecCertificateCopyData(serverCert) as Data

if serverCertData == pinnedCertData {

completionHandler(.useCredential, URLCredential(trust: serverTrust))

} else {

completionHandler(.cancelAuthenticationChallenge, nil)

}

}

}

## Pinning Update Strategy

Certificate pinning breaks when you rotate certificates. Plan for updates:

  * Pin against the public key, not the full certificate. This allows CA re-issuance with the same key.

  * Include a backup pin for a second CA in case the primary certificate expires.

  * Push new pins through app updates well before certificate expiry.

  * Consider using certificate transparency instead of pinning for some environments.




## Secure Storage

Mobile OS platforms provide secure storage mechanisms that encrypt data at rest.

## Android Encrypted SharedPreferences

// Using EncryptedSharedPreferences

val masterKey = MasterKey.Builder(context)

.setKeyScheme(MasterKey.KeyScheme.AES256_GCM)

.build()

val sharedPreferences = EncryptedSharedPreferences.create(

context,

"secure_prefs",

masterKey,

EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,

EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM

)

sharedPreferences.edit()

.putString("auth_token", token)

.apply()

## Android Keystore

The Android Keystore stores cryptographic keys in a hardware-backed environment (TEE or StrongBox). Extracting the key requires physical device access and specialized tools.

// Generate a key in Android Keystore

val keyGenerator = KeyGenerator.getInstance(

KeyProperties.KEY_ALGORITHM_AES,

"AndroidKeyStore"

)

val spec = KeyGenParameterSpec.Builder(

"app_key",

KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT

)

.setBlockModes(KeyProperties.BLOCK_MODE_GCM)

.setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)

.setKeySize(256)

.build()

keyGenerator.init(spec)

val secretKey = keyGenerator.generateKey()

## iOS Keychain

iOS Keychain is the secure storage mechanism on Apple devices. It encrypts data using device-specific keys that never leave the Secure Enclave.

// Store data in Keychain

let query: [String: Any] = [

kSecClass as String: kSecClassGenericPassword,

kSecAttrAccount as String: "auth_token",

kSecAttrService as String: "com.example.app",

kSecValueData as String: tokenData,

kSecAttrAccessControl as String: SecAccessControlCreateWithFlags(

nil,

kSecAttrApplicationTag,

.biometryCurrentSet,

nil

)

]

SecItemAdd(query as CFDictionary, nil)

## Runtime Protection

Runtime protection defends against tampering while the app is running.

## Root/Jailbreak Detection

// Android root detection

fun isDeviceRooted(): Boolean {

val rootPaths = listOf(

"/system/app/Superuser.apk",

"/sbin/su",

"/system/bin/su",

"/system/xbin/su",

"/data/local/xbin/su",

"/data/local/bin/su",

"/system/sd/xbin/su",

"/system/bin/failsafe/su",

"/data/local/su"

)

return rootPaths.any { File(it).exists() }

}

// iOS jailbreak detection

func isDeviceJailbroken() -> Bool {

let jbPaths = [

"/Applications/Cydia.app",

"/Library/MobileSubstrate/MobileSubstrate.dylib",

"/bin/bash",

"/usr/sbin/sshd",

"/etc/apt",

"/private/var/lib/apt/"

]

return jbPaths.contains { FileManager.default.fileExists(atPath: $0) }

}

Never terminate the app immediately on detecting a compromised device. This gives attackers a signal to bypass your detection. Instead, degrade functionality silently or report the event to your backend.

## Debugger Detection

// iOS debugger detection

func isDebuggerAttached() -> Bool {

var name: [Int32] = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]

var info = kinfo_proc()

var infoSize = MemoryLayout.size

sysctl(&name;, 4, &info;, &infoSize;, nil, 0)

return (info.kp_proc.p_flag & P_TRACED) != 0

}

## Conclusion

Mobile security requires defense in depth. Obfuscate your code to slow down reverse engineering. Pin certificates to prevent MITM attacks. Use platform-provided secure storage for sensitive data. Add runtime protection against root/jailbreak and debugging. Most importantly, follow the OWASP Mobile Top 10 as your baseline and validate controls with regular penetration testing.

**See also:** [Webhook Security Best Practices](</en/security/webhook-security.html>), [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Container Security Best Practices](</en/security/container-security.html>).

**See also:** [Webhook Security Best Practices](</en/security/webhook-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>)

**See also:** [Webhook Security Best Practices](</en/security/webhook-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>)

**See also:** [Webhook Security Best Practices](</en/security/webhook-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>)

**See also:** [Webhook Security Best Practices](</en/security/webhook-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>)

**See also:** [Webhook Security Best Practices](</en/security/webhook-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>)
