#[derive(thiserror::Error, Debug)]
pub enum SeverityKind {
    #[error("An empty quoted key is allowed, but it is not recommended")]
    KeyEmpty,
}

#[derive(Debug)]
pub struct Severity {
    pub kind: SeverityKind,
    pub level: tombi_config::SeverityLevel,
    pub range: tombi_text::Range,
}

impl tombi_diagnostic::SetDiagnostics for Severity {
    fn set_diagnostics(self, diagnostics: &mut Vec<tombi_diagnostic::Diagnostic>) {
        match self.level {
            tombi_config::SeverityLevel::Error => {
                diagnostics.push(tombi_diagnostic::Diagnostic::new_error(
                    self.kind.to_string(),
                    self.range,
                ));
            }
            tombi_config::SeverityLevel::Warn => {
                diagnostics.push(tombi_diagnostic::Diagnostic::new_warning(
                    self.kind.to_string(),
                    self.range,
                ));
            }
            tombi_config::SeverityLevel::Off => {}
        }
    }
}
