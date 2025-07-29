fn main() {
    // On macOS, Python extension modules are expected to be built as dynamic
    // libraries with undefined symbols resolved at load time by the Python
    // interpreter. The usual way PyO3 supplies this is via its build script,
    // but depending on the build graph `cargo` can occasionally drop these
    // flags when the crate is built directly (e.g. with `cargo build`).
    // Supplying them here guarantees successful linkage when building the
    // `cdylib` on macOS.
    #[cfg(target_os = "macos")]
    {
        println!("cargo:rustc-link-arg=-undefined");
        println!("cargo:rustc-link-arg=dynamic_lookup");
    }
}
