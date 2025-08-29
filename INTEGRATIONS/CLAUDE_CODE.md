# Claude Code Integration

Path: `external/claude-code` (git submodule)
Upstream: https://github.com/anthropics/claude-code (branch: main)
Integration Method: Git submodule (pointer to specific upstream commit).

## Rationale
Using a submodule preserves a clean boundary, reduces repository size, and allows pinning to known-good commits while enabling rapid upstream updates.

## Initial Setup (one-time after clone)
```bash
git submodule update --init --recursive
```

## Updating to Latest Upstream
Review upstream changes first:
```bash
cd external/claude-code
git fetch origin
git log --oneline HEAD..origin/main | head
cd ../../
```
Update submodule to latest main and commit pointer:
```bash
git submodule update --remote --merge external/claude-code
git add external/claude-code
git commit -m "chore(claude-code): update submodule to latest main"
```
(Alternative) Fast-forward only:
```bash
git submodule foreach 'git checkout main && git pull --ff-only'
```

## Removing the Submodule (if ever required)
```bash
git rm -f external/claude-code
rm -rf .git/modules/external/claude-code
sed -i.bak '/external\/claude-code/d' .gitmodules
rm .gitmodules.bak
git commit -m "chore: remove claude-code submodule"
```

## Contributing Back Upstream
1. Enter submodule: `cd external/claude-code`
2. Create branch against upstream repository fork (if you have push rights):
```bash
git checkout -b feature/your-change
# make changes
git commit -am "feat: your change"
git push origin feature/your-change
```
3. Open PR in upstream repo.
4. Update pinned commit in this repository after upstream merges.

## CI Considerations
GitHub Actions must checkout submodules:
```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive
```

## Security & Provenance
- Submodule pins a specific commit ensuring reproducibility.
- Always review diffs before updating pointer.
- Consider enabling Dependabot or scheduled workflows to surface new upstream commits for review.

## License & Attribution
(Placeholder) Upstream license will be summarized here. Ensure compatibility with this repository's license. Add any required NOTICE text to `/NOTICE`.

## Related Files
- `.gitmodules`
- `NOTICE` (attribution)
- `.github/workflows/claude-code-sync.yml`

## System Prompt Alignment
This integration operates under directives in `TEQUMSA_L100_SYSTEM_PROMPT.md`. Update scripts should log significant lattice-impacting changes to `logs/CONSCIOUSNESS_LOG.md`.