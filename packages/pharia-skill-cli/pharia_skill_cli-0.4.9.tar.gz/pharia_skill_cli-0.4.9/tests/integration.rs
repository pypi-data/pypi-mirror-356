use std::{env, fs::File, io::Write, path::Path};

use assert_cmd::Command;

#[test]
fn invalid_args() {
    let mut cmd = Command::cargo_bin("pharia-skill-cli").unwrap();
    let cmd = cmd
        .arg("publish")
        .arg("-R")
        .arg("dummy-registry")
        .arg("-r")
        .arg("dummy-repo")
        .arg("-u")
        .arg("dummy_user")
        .arg("-p")
        .arg("dummy_token")
        .arg("dummy.wasm");
    cmd.assert().failure();
}

fn wasm_file() -> &'static Path {
    let path = Path::new("./skills/test-skill.wasm");
    if !path.exists() {
        let mut file = File::create(path).unwrap();
        let content = wat::parse_str("(module)").unwrap();
        file.write_all(&content).unwrap();
    }
    path
}

#[test]
fn publish_minimal_args() {
    drop(dotenvy::dotenv());
    let path = wasm_file();
    let mut cmd = Command::cargo_bin("pharia-skill-cli").unwrap();
    let cmd = cmd
        .arg("publish")
        .arg(path)
        .arg("-t")
        .arg("0.0.1")
        .env(
            "SKILL_REGISTRY",
            env::var("SKILL_REGISTRY").expect("SKILL_REGISTRY must be set."),
        )
        .env(
            "SKILL_REPOSITORY",
            env::var("SKILL_REPOSITORY").expect("SKILL_REPOSITORY must be set."),
        )
        .env(
            "SKILL_REGISTRY_USER",
            env::var("SKILL_REGISTRY_USER").expect("SKILL_REGISTRY_USER must be set."),
        )
        .env(
            "SKILL_REGISTRY_TOKEN",
            env::var("SKILL_REGISTRY_TOKEN").expect("SKILL_REGISTRY_TOKEN must be set."),
        );
    cmd.assert().success();
}
