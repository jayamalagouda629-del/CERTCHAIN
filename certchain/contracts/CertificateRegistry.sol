// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// Stores only hash + USN + IPFS CID. No student PII.
contract CertificateRegistry {
    struct CertificateRecord {
        string studentUSN;
        string ipfsCID;
        uint256 issueTimestamp;
        address issuedBy;
        bool isRevoked;
        uint256 revokedAt;
    }

    address public owner;
    mapping(address => bool) public isIssuer;               // HOD / Exam Cell wallets
    mapping(bytes32 => CertificateRecord) private records;
    mapping(string => bytes32) public latestHashOfUSN;      // used by QR lookup
    uint256 public totalCertificates;

    event CertificateIssued(bytes32 indexed certHash, string usn, string ipfsCID, address indexed by);
    event CertificateRevoked(bytes32 indexed certHash, address indexed by);
    event IssuerChanged(address indexed account, bool allowed);

    modifier onlyOwner() { require(msg.sender == owner, "Not owner"); _; }
    modifier onlyIssuer() { require(isIssuer[msg.sender], "Not authorized issuer"); _; }

    constructor() { owner = msg.sender; isIssuer[msg.sender] = true; emit IssuerChanged(msg.sender, true); }

    function setIssuer(address a, bool allowed) external onlyOwner {
        isIssuer[a] = allowed; emit IssuerChanged(a, allowed);
    }

    function issueCertificate(bytes32 certHash, string calldata usn, string calldata ipfsCID) external onlyIssuer {
        require(records[certHash].issueTimestamp == 0, "Already issued");
        records[certHash] = CertificateRecord(usn, ipfsCID, block.timestamp, msg.sender, false, 0);
        latestHashOfUSN[usn] = certHash;
        totalCertificates++;
        emit CertificateIssued(certHash, usn, ipfsCID, msg.sender);
    }

    function revokeCertificate(bytes32 certHash) external onlyIssuer {
        CertificateRecord storage r = records[certHash];
        require(r.issueTimestamp != 0, "Unknown certificate");
        require(!r.isRevoked, "Already revoked");
        r.isRevoked = true; r.revokedAt = block.timestamp;
        emit CertificateRevoked(certHash, msg.sender);
    }

    /// Gasless read (eth_call)
    function verifyCertificate(bytes32 certHash) external view returns (
        bool exists, bool revoked, string memory usn, string memory ipfsCID, uint256 issuedAt, uint256 revokedAt
    ) {
        CertificateRecord storage r = records[certHash];
        return (r.issueTimestamp != 0, r.isRevoked, r.studentUSN, r.ipfsCID, r.issueTimestamp, r.revokedAt);
    }
}
