module.exports = {
  branches: [
    "main",
    {
      name: "develop",
      prerelease: true,
    },
    {
      name: "**/+([0-9])[-]*",
      prerelease: "issue-${name}",
    },
  ],
  tagFormat: "${version}",
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/github",
    [
      "@semantic-release/exec",
      {
        verifyRelease: "echo nextRelease.version is ${nextRelease.version} && echo -n ${nextRelease.version} > VERSION",
      },
    ],
  ],
};
