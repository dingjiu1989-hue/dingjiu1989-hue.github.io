---
title: "Blockchain and Smart Contract Security"
description: "Smart contract vulnerabilities including reentrancy and oracle manipulation, plus auditing tools, formal verification, and wallet security."
date: 2026-03-03
board: security
url: https://dingjiu1989-hue.github.io/en/security/blockchain-security.html
---

# Blockchain and Smart Contract Security

Blockchain and smart contract security presents unique challenges. Once deployed, smart contracts are immutable. A vulnerability in a contract can result in millions of dollars in losses with no recourse. This article covers common smart contract vulnerabilities, auditing tools and techniques, formal verification, and wallet security.

## Common Smart Contract Vulnerabilities

## Reentrancy

Reentrancy is the most infamous smart contract vulnerability. It occurs when a contract calls an external contract before updating its own state, allowing the external contract to recursively call back into the original contract before the first invocation completes.

// VULNERABLE: Reentrancy

contract VulnerableWithdraw {

mapping(address => uint) public balances;

function withdraw(uint amount) public {

require(balances[msg.sender] >= amount);

// STATE NOT UPDATED BEFORE EXTERNAL CALL

(bool success, ) = msg.sender.call{value: amount}("");

require(success, "Transfer failed");

balances[msg.sender] -= amount; // TOO LATE

}

}

An attacker contract can exploit this by calling `withdraw` repeatedly from its `receive` function, draining all funds before the balance is updated.

**Prevention** :

  * Use the checks-effects-interactions pattern: update state before making external calls.

  * Use OpenZeppelin's ReentrancyGuard modifier.




// SAFE: Checks-Effects-Interactions

contract SafeWithdraw {

using ReentrancyGuard for *;

mapping(address => uint) public balances;

function withdraw(uint amount) public nonReentrant {

require(balances[msg.sender] >= amount);

balances[msg.sender] -= amount; // Update state first

(bool success, ) = msg.sender.call{value: amount}("");

require(success, "Transfer failed");

}

}

## Oracle Manipulation

Smart contracts rely on oracles to bring off-chain data (price feeds, randomness) on-chain. If an oracle is manipulated, contracts depending on that data behave incorrectly.

**Flash loan attacks** : An attacker borrows a large amount of tokens, trades them to manipulate the pool price, then exploits a contract that reads the manipulated price. The attacker repays the flash loan in the same transaction.

**Prevention** :

  * Use decentralized oracle networks like Chainlink that aggregate data from multiple sources.

  * Implement time-weighted average prices (TWAP) rather than spot prices.

  * Add sanity checks and circuit breakers for price movements beyond normal ranges.




// Using Chainlink price feed with TWAP protection

contract SafePrice {

AggregatorV3Interface internal priceFeed;

constructor() {

priceFeed = AggregatorV3Interface(

0x... // Chainlink ETH/USD feed address

);

}

function getSafePrice() public view returns (uint) {

// Use historical data to prevent flash loan manipulation

uint price1 = getRoundData(roundsAgo: 1);

uint price2 = getRoundData(roundsAgo: 2);

uint price3 = getRoundData(roundsAgo: 3);

return (price1 + price2 + price3) / 3;

}

}

## Front-Running

Transactions in the mempool are visible to all. MEV (Maximal Extractable Value) bots monitor the mempool and submit transactions ahead of profitable trades.

**Prevention** :

  * Use commit-reveal schemes where users commit to an action in one transaction and reveal details in another.

  * Set slippage tolerances to limit the impact of price changes.

  * Use private transaction relayers (Flashbots, MEV Blocker).




## Integer Overflow and Underflow

While Solidity 0.8+ includes built-in overflow checking via `unchecked` blocks, older versions required SafeMath. Always use SafeMath or Solidity 0.8+ for arithmetic.

// Solidity 0.8+ automatically reverts on overflow

uint256 max = type(uint256).max;

uint256 result = max + 1; // Reverts

// Use unchecked only when you know bounds are safe

unchecked {

uint256 result = max + 1; // Wraps around (use with caution)

}

## Access Control Vulnerabilities

Improper access control allows unauthorized users to call privileged functions. The Parity multi-sig wallet hack (2017) lost 30 million dollars due to an unprotected `initWallet` function.

**Prevention** :

  * Use OpenZeppelin's Ownable and AccessControl libraries.

  * Never rely on `tx.origin` for authentication.

  * Follow the principle of least privilege for admin functions.

  * Use multi-signature wallets for privileged operations.




// Secure access control with OpenZeppelin

import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureContract is AccessControl {

bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

constructor() {

_grantRole(DEFAULT_ADMIN_ROLE, msg.sender);

_grantRole(PAUSER_ROLE, msg.sender);

}

function pause() public onlyRole(PAUSER_ROLE) {

_pause();

}

}

## Smart Contract Auditing

Auditing is the primary defense against smart contract vulnerabilities. A thorough audit combines automated scanning with manual review.

## Automated Auditing Tools

  * **Slither** : Static analysis framework for Solidity. Detects common vulnerabilities, generates contract inheritance graphs, and identifies dangerous patterns.

  * **Mythril** : Security analysis tool that uses symbolic execution to find vulnerabilities.

  * **Echidna** : Fuzzing tool that tests contract properties using random inputs.




## Slither analysis

slither my_contract.sol --print human-summary

## Run specific detectors

slither my_contract.sol --detect reentrancy-eth,reentrancy-no-eth

## Mythril analysis

myth analyze my_contract.sol --solc-json solc.json

## Property-Based Fuzzing with Foundry

Foundry is a modern Solidity testing framework that supports fuzz testing and invariant testing.

// Foundry fuzz test

contract TestToken is Test {

Token token;

function setUp() public {

token = new Token();

}

// Fuzz test: total supply should never decrease

function testTotalSupplyNeverDecreases(uint256 amount) public {

uint256 before = token.totalSupply();

vm.assume(amount > 0 && amount < 1_000_000 ether);

vm.prank(address(0xdead));

token.mint(amount);

assertGe(token.totalSupply(), before);

}

}

## Manual Review Checklist

Automated tools catch common patterns but miss business logic flaws. Manual review is essential.

  * **Access control** : Can every user call every function? Are admin functions protected?

  * **State consistency** : Are internal bookkeeping values consistent with actual token balances?

  * **Rounding** : Are there rounding errors that can accumulate over many operations?

  * **Upgradeability** : Can the admin arbitrarily steal funds via proxy upgrade?

  * **Emergency stop** : Can the contract be paused during an attack? Is the pause function itself protected?

  * **Token handling** : Does the contract handle non-standard ERC-20 tokens (USDT, fee-on-transfer)?




## Formal Verification

Formal verification mathematically proves that a contract satisfies specified properties. It is the highest assurance level for smart contract security.

## Tools

  * **Certora Prover** : Automated formal verification platform with property specification language.

  * **KEVM / K Framework** : Executable formal semantics of the EVM.

  * **Halmos** : Symbolic testing tool for Foundry-compatible projects.




// Certora property specification

rule total_supply_invariant() {

uint256 supply_before = totalSupply();

// Any operation

method f; env e;

calldataarg args;

f(e, args);

uint256 supply_after = totalSupply();

// For non-mint operations, supply must not increase

assert supply_after >= supply_before;

}

Formal verification is most valuable for high-value contracts (DeFi protocols, bridges, stablecoins) where failure is catastrophic.

## Wallet Security

User wallets are a major attack vector. Protecting wallet infrastructure is critical for any blockchain application.

## Key Management

  * Never store private keys in plaintext.

  * Use hardware security modules (HSMs) or cloud KMS for server-side keys.

  * Implement multi-party computation (MPC) for distributed key management.




## EIP-712 Structured Data Signing

Use typed data signing (EIP-712) to make signed data readable in wallets, reducing phishing risk.

// EIP-712 typed data

struct Permit {

address owner;

address spender;

uint256 value;

uint256 nonce;

uint256 deadline;

}

bytes32 constant PERMIT_TYPEHASH = keccak256(

"Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)"

);

## Conclusion

Smart contract security requires a multi-layered approach. Understand common vulnerabilities like reentrancy, oracle manipulation, and front-running. Use automated analysis tools like Slither and Mythril. Invest in formal verification for high-value contracts. Implement rigorous access control and follow patterns like checks-effects-interactions. Finally, secure the wallet infrastructure that interacts with your contracts. In the immutable world of blockchain, security is not optional.

**See also:** [Container Security Best Practices](</en/security/container-security.html>), [Security Log Management](</en/security/log-management-security.html>), [Webhook Security Best Practices](</en/security/webhook-security.html>).

**See also:** [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Vulnerability Scanning: Tools and Workflows](</en/security/vulnerability-scanning.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Vulnerability Scanning: Tools and Workflows](</en/security/vulnerability-scanning.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Vulnerability Scanning: Tools and Workflows](</en/security/vulnerability-scanning.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Vulnerability Scanning: Tools and Workflows](</en/security/vulnerability-scanning.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Vulnerability Scanning: Tools and Workflows](</en/security/vulnerability-scanning.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)
