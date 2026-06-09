---
name: CKBCellBuildRecipe
description: "∀ ckb-std cell-script crate ⇒ workspace dep MUST enable `ckb-types` + `allocator` features ∧ ✗ explicit `extern crate alloc` @ crate root (allocator feature provides it) ∧ blake2b ⇒ `blake2b-ref 0.3` w/ personal \"ckb-default-hash\" ¬ `ckb_std::high_level::blake2b_256` (not in 0.16) ∧ bls12_381 0.8 ⇒ pair w/ sha2 = 0.9 (digest 0.9 ABI) ¬ 0.10 ∧ enum w/ payload variant ⇒ ✗ primitive cast `as i8` ⇒ flatten variants ∨ derive Discriminant. Receipts: workspace Cargo.toml at vibeswap/contracts-ckb 2026-06-09 first-green build."
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·ckb-cell-build-recipe]**

## ⚙ Rule

∀ ckb-std cell crate ⇒ build recipe:

✓ workspace `ckb-std = { version="0.16", default-features=false, features=["ckb-types","allocator"] }`
✓ `default_alloc!()` macro provides `extern crate alloc` ⇒ ✗ duplicate at crate root
✓ blake2b ⇒ `blake2b-ref = "0.3"` w/ `personal(b"ckb-default-hash")` (ckb-std 0.16 ¬ export blake2b)
✓ bls12_381 = "0.8" ⇒ sha2 = "0.9" (digest 0.9 ABI) ¬ "0.10" (digest 0.10 mismatch)
✓ bls12_381 0.8 ⇒ enable `experimental` feature for `hash_to_curve`
✓ `#[repr(i8)]` enum w/ payload variant ⇒ ✗ `e as i8` primitive cast ⇒ flatten variants ∨ derive

✗ `pub use ckb_hash::new_blake2b` — ckb-std 0.16 has type_id internal use only, ¬ public re-export
✗ `extern crate alloc;` at crate root when `default_alloc!()` invoked
✗ sha2 0.10 paired w/ bls12_381 0.8 (digest version mismatch ⇒ trait-bound error cascade)
✗ `BlsLibError(i8)` payload variant w/ `as i8` cast — non-primitive cast

## 🎯 The receipts

2026-06-09 first-green build of vibeswap/contracts-ckb workspace under MSVC toolchain.

| Failure mode | Root cause | Fix |
|---|---|---|
| `unresolved import ckb_std::high_level` | workspace `default-features=false` w/ no features ⇒ `ckb-types` feature off | add `features=["ckb-types","allocator"]` |
| `could not find buddy_alloc in $crate` | same — `allocator` feature off | same |
| `name alloc defined multiple times` | explicit `extern crate alloc;` + `default_alloc!()` both | strip explicit (sed `/^extern crate alloc;$/d`) |
| `unresolved import bls12_381::hash_to_curve` | bls12_381 `experimental` off | add to workspace bls12_381 features |
| `digest::Update not satisfied` (4×) | sha2 0.10 → digest 0.10; bls12_381 0.8 wants digest 0.9 | pin sha2 = "0.9" |
| `cannot find function blake2b_256 in ckb_std::high_level` | 0.16 has no public blake2b | add `blake2b-ref` dep + Blake2bBuilder |
| `non-primitive cast: Error as i8` | enum variant carried payload | flatten to fieldless |

## 🎯 The skeleton (canonical per-cell Cargo.toml)

```toml
[package]
name = "my-cell-type-script"
version.workspace = true
edition.workspace = true
authors.workspace = true
license.workspace = true
publish.workspace = true

[[bin]]
name = "my-cell-type-script"
path = "src/main.rs"

[dependencies]
ckb-std = { workspace = true }
heapless = { workspace = true }
# Cell-specific deps (blake2b-ref iff cell hashes; bls-verify iff verifies sigs)
```

## 🎯 The workspace declaration

```toml
[workspace.dependencies]
ckb-std = { version = "0.16", default-features = false, features = ["ckb-types", "allocator"] }
bls12_381 = { version = "0.8", default-features = false, features = ["alloc", "pairings", "groups", "experimental"] }
heapless = { version = "0.8", default-features = false }
```

## 🎯 The host-toolchain prerequisites (Windows)

1. VS Build Tools 14.44+ MSVC linker
   `winget install Microsoft.VisualStudio.2022.BuildTools --override "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"`
2. Invoke cargo via batch file that pre-calls vcvars64.bat:
   ```bat
   @echo off
   call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
   cargo build --release --target riscv64imac-unknown-none-elf -p <crate>
   ```
3. Without vcvars64 active, rustc picks `C:\Program Files\Git\usr\bin\link.exe` (GNU coreutils `link`) instead of MSVC `link.exe` ⇒ "extra operand" error

## 🪝 Triggers

- ∀ new CKB cell crate scaffold ⇒ apply this recipe
- ∀ ckb-std bump ⇒ re-verify feature names + blake2b path
- ∀ bls12_381 bump ⇒ re-verify paired sha2/digest version

## 🔗 Composes-with

- [F·spec-vs-deployed-severity-calibration] — spec-only cells w/ TODO debt = LOW pre-deploy; this recipe is what closes deploy-prep cycle
- [F·code-comment-why-only] — TODOs in the original scaffolds violated this; build now grounds them
- [P·six-commandment-autonomous-loop] C5 REVIEW — this primitive IS the C5 output of the 2026-06-09 build epoch

## 📦 Receipts

- 2026-06-09 08:57 ET — primitive-cell-type-script first green build (after adding features to workspace ckb-std)
- 2026-06-09 08:58 ET — vibeswap-canonical-token-type-script green
- 2026-06-09 09:00–09:05 ET — all 26 cell binaries compiled to riscv64imac-unknown-none-elf
- target/riscv64imac-unknown-none-elf/release: 26 ELF binaries, sizes 12K–343K, hash-anchored to commit on master post-78059ec2
