import { readFile, writeFile } from "node:fs/promises";

const repo = process.env.GITHUB_REPOSITORY || "Matthew-Eucaristo/Matthew-Eucaristo";
const token = process.env.GITHUB_TOKEN;
const readmePath = "README.md";

const missions = [
  {
    name: "Deploy GG.AI Infra",
    signal: "AI agents + DevOps",
  },
  {
    name: "Train RL Game Agent",
    signal: "Rainbow DQN + game AI",
  },
  {
    name: "Prototype Unreal System",
    signal: "Gameplay + tooling",
  },
  {
    name: "Ship Web3 Game Loop",
    signal: "Smart contracts + play",
  },
];

const missionByKey = new Map(missions.map((mission) => [normalize(mission.name), mission]));
const missionIndex = new Map(missions.map((mission, index) => [mission.name, index]));

function normalize(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function issueUrl(mission) {
  const title = `Bingo Mission: ${mission.name}`;
  const body = `Mission: ${mission.name}\n\nI vote for this Matthew.SYS mission.`;
  const params = new URLSearchParams({ title, body });

  return `https://github.com/${repo}/issues/new?${params.toString()}`;
}

function findMission(issue) {
  const titleMatch = issue.title?.match(/^Bingo Mission:\s*(.+)$/i);
  const bodyMatch = issue.body?.match(/^Mission:\s*(.+)$/im);
  const candidates = [titleMatch?.[1], bodyMatch?.[1], issue.title, issue.body].filter(Boolean);

  for (const candidate of candidates) {
    const normalizedCandidate = normalize(candidate);

    if (missionByKey.has(normalizedCandidate)) {
      return missionByKey.get(normalizedCandidate);
    }

    for (const [key, mission] of missionByKey) {
      if (normalizedCandidate.includes(key)) {
        return mission;
      }
    }
  }

  return null;
}

async function fetchIssues() {
  if (!token) {
    console.warn("GITHUB_TOKEN was not provided; mission board will render without remote votes.");
    return [];
  }

  const issues = [];

  for (let page = 1; page <= 5; page += 1) {
    const response = await fetch(
      `https://api.github.com/repos/${repo}/issues?state=all&per_page=100&page=${page}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
        },
      },
    );

    if (!response.ok) {
      throw new Error(`GitHub API returned ${response.status}: ${await response.text()}`);
    }

    const pageIssues = await response.json();
    issues.push(...pageIssues.filter((issue) => !issue.pull_request));

    if (pageIssues.length < 100) {
      break;
    }
  }

  return issues;
}

function buildVoteState(issues) {
  const latestVoteByUser = new Map();

  for (const issue of issues.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))) {
    const mission = findMission(issue);
    const user = issue.user?.login;

    if (mission && user) {
      latestVoteByUser.set(user, mission.name);
    }
  }

  const votes = new Map(missions.map((mission) => [mission.name, new Set()]));

  for (const [user, missionName] of latestVoteByUser) {
    votes.get(missionName)?.add(user);
  }

  return votes;
}

function buildMissionBoard(votes) {
  const voteCounts = missions.map((mission) => ({
    ...mission,
    votes: votes.get(mission.name)?.size || 0,
  }));
  const totalVoters = voteCounts.reduce((total, mission) => total + mission.votes, 0);
  const leader = [...voteCounts].sort(
    (a, b) => b.votes - a.votes || missionIndex.get(a.name) - missionIndex.get(b.name),
  )[0];
  const command = totalVoters > 0 ? leader.name : "Awaiting first vote";
  const rows = voteCounts
    .map((mission) => `| [${mission.name}](${issueUrl(mission)}) | ${mission.signal} | ${mission.votes} |`)
    .join("\n");
  const syncedAt = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

  return `<!-- mission-board:start -->
<p align="center">
  <strong>Current command:</strong> <code>${command}</code> /
  <strong>Total voters:</strong> <code>${totalVoters}</code>
</p>

| Mission | Signal | Unique voters |
| --- | --- | ---: |
${rows}

<sub>Last vote per GitHub user counts. Last sync: ${syncedAt}.</sub>
<!-- mission-board:end -->`;
}

const readme = await readFile(readmePath, "utf8");

if (!readme.includes("<!-- mission-board:start -->") || !readme.includes("<!-- mission-board:end -->")) {
  throw new Error("README.md is missing the mission board markers.");
}

const issues = await fetchIssues();
const votes = buildVoteState(issues);
const missionBoard = buildMissionBoard(votes);
const updatedReadme = readme.replace(
  /<!-- mission-board:start -->[\s\S]*?<!-- mission-board:end -->/,
  missionBoard,
);

if (updatedReadme === readme) {
  console.log("Mission board is already up to date.");
} else {
  await writeFile(readmePath, updatedReadme);
  console.log("Mission board updated.");
}
