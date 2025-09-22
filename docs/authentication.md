# Authentication System

This document describes the comprehensive authentication system implemented for the Enterprise CRM, which includes OAuth 2.0, OpenID Connect, MFA, device fingerprinting, and WebAuthn support.

## Features Implemented

### 1. OAuth 2.0 + OpenID Connect
- Standard OAuth 2.0 token endpoints for authentication
- JWT-based access and refresh tokens
- OpenID Connect support for identity verification
- Secure token generation with configurable expiration
- Token refresh mechanism

### 2. Server-side Sessions with Encrypted Storage
- Encrypted session data storage
- Session expiration management
- Secure session invalidation
- Session data encryption using Fernet symmetric encryption

### 3. MFA (Multi-Factor Authentication)
- Time-based one-time passwords (TOTP)
- Email/SMS-based verification codes
- Configurable expiration times
- Single-use code validation

### 4. Device Fingerprinting and Monitoring
- Device identification and tracking
- User agent and IP address monitoring
- Location tracking (optional)
- Device session management

### 5. WebAuthn for Passwordless Authentication
- FIDO2/WebAuthn protocol support
- PublicKeyCredential registration
- Cryptographic authentication challenges
- Device-bound credentials

## API Endpoints

### Authentication Endpoints
- `POST /api/superadmin/security/auth/token` - OAuth 2.0 token endpoint
- `POST /api/superadmin/security/auth/refresh` - Refresh access token
- `POST /api/superadmin/security/auth/mfa/generate` - Generate MFA code
- `POST /api/superadmin/security/auth/mfa/verify` - Verify MFA code
- `POST /api/superadmin/security/auth/webauthn/register` - Register WebAuthn credential
- `POST /api/superadmin/security/auth/webauthn/authenticate` - Authenticate with WebAuthn
- `POST /api/superadmin/security/auth/session` - Create session
- `DELETE /api/superadmin/security/auth/session/{session_id}` - Invalidate session
- `GET /api/superadmin/security/auth/devices` - List user devices
- `GET /api/superadmin/security/auth/me` - Get current user info

## Security Features

### Token Security
- JWT tokens with HMAC-SHA256 signing
- Configurable token expiration times
- Refresh token rotation
- Token revocation support

### Session Security
- Encrypted session storage
- Session expiration enforcement
- Device binding
- Session hijacking prevention

### MFA Security
- Time-limited codes (5-minute expiration)
- Single-use verification
- Multiple delivery methods
- Rate limiting protection

### WebAuthn Security
- Cryptographic challenge-response authentication
- Device-bound credentials
- Phishing-resistant authentication
- Biometric authentication support

## Implementation Details

### Dependencies
The authentication system requires the following Python packages:
- `python-jose` for JWT handling
- `cryptography` for encryption
- `pyjwt` for token processing
- `passlib` for password hashing (future implementation)

### Configuration
Key configuration parameters:
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT signing algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration (30 minutes)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration (7 days)
- `ENCRYPTION_KEY` - Session data encryption key

### Data Models
The system introduces several new data models:
- `AuthToken` - Access and refresh token container
- `TokenData` - Decoded token information
- `DeviceInfo` - Device fingerprinting data
- `MFACode` - MFA code storage
- `WebAuthnCredential` - WebAuthn credential storage

## Usage Examples

### OAuth 2.0 Authentication Flow
1. Client requests token with username/password
2. Server validates credentials and generates JWT tokens
3. Client uses access token for API requests
4. Client refreshes token when access token expires

### MFA Flow
1. User authenticates with username/password
2. System generates and sends MFA code
3. User provides MFA code for verification
4. System grants access upon successful verification

### WebAuthn Flow
1. User registers WebAuthn credential
2. System stores public key and credential ID
3. User authenticates with WebAuthn credential
4. System verifies cryptographic signature

## Future Enhancements

### Planned Improvements
- Integration with external identity providers (Google, Microsoft, etc.)
- SMS-based MFA delivery
- Push notification MFA
- Biometric authentication enhancements
- Certificate-based authentication
- SAML support for enterprise integration

### Security Enhancements
- Rate limiting for authentication attempts
- Account lockout after failed attempts
- IP-based access restrictions
- Geolocation-based access controls
- Behavioral analytics for anomaly detection

## Testing

The authentication system includes comprehensive tests:
- Endpoint accessibility verification
- Token generation and validation
- MFA code generation and verification
- WebAuthn registration and authentication
- Session management
- Device fingerprinting

All tests can be run using the test suite in the `tests` directory.