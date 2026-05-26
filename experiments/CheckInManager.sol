// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CheckInManager {
    // Mapping: user address -> block number -> commit hash
    mapping(address => mapping(uint256 => string)) private _commits;

    // Event emitted when a user submits a commit
    event CommitSubmitted(address indexed user, uint256 indexed blockNumber, string commitHash);

    // Read function to fetch a specific commit by address and block number
    function getCommit(address user, uint256 blockNumber) public view returns (string memory) {
        return _commits[user][blockNumber];
    }

    // Write function for users to submit their commit hash
    function submitCommit(string memory commitHash) public {
        require(_verifyCommit(commitHash), "Commit verification failed");
        uint256 blockNumber = block.number;
        _commits[msg.sender][blockNumber] = commitHash;
        emit CommitSubmitted(msg.sender, blockNumber, commitHash);
    }

    // Private function to mock commit verification
    function _verifyCommit(string memory commitHash) private pure returns (bool) {
        // Mock logic: accept any non-empty commit hash
        return bytes(commitHash).length > 0;
    }
}
