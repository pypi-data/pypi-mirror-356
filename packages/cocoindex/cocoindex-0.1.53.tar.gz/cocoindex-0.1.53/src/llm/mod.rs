use std::borrow::Cow;

use anyhow::Result;
use async_trait::async_trait;
use schemars::schema::SchemaObject;
use serde::{Deserialize, Serialize};

use crate::base::json_schema::ToJsonSchemaOptions;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum LlmApiType {
    Ollama,
    OpenAi,
    Gemini,
    Anthropic,
    LiteLlm,
    OpenRouter,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LlmSpec {
    api_type: LlmApiType,
    address: Option<String>,
    model: String,
}

#[derive(Debug)]
pub enum OutputFormat<'a> {
    JsonSchema {
        name: Cow<'a, str>,
        schema: Cow<'a, SchemaObject>,
    },
}

#[derive(Debug)]
pub struct LlmGenerateRequest<'a> {
    pub system_prompt: Option<Cow<'a, str>>,
    pub user_prompt: Cow<'a, str>,
    pub output_format: Option<OutputFormat<'a>>,
}

#[derive(Debug)]
pub struct LlmGenerateResponse {
    pub text: String,
}

#[async_trait]
pub trait LlmGenerationClient: Send + Sync {
    async fn generate<'req>(
        &self,
        request: LlmGenerateRequest<'req>,
    ) -> Result<LlmGenerateResponse>;

    fn json_schema_options(&self) -> ToJsonSchemaOptions;
}

mod anthropic;
mod gemini;
mod ollama;
mod openai;
mod litellm;
mod openrouter;

pub async fn new_llm_generation_client(spec: LlmSpec) -> Result<Box<dyn LlmGenerationClient>> {
    let client = match spec.api_type {
        LlmApiType::Ollama => {
            Box::new(ollama::Client::new(spec).await?) as Box<dyn LlmGenerationClient>
        }
        LlmApiType::OpenAi => {
            Box::new(openai::Client::new(spec).await?) as Box<dyn LlmGenerationClient>
        }
        LlmApiType::Gemini => {
            Box::new(gemini::Client::new(spec).await?) as Box<dyn LlmGenerationClient>
        }
        LlmApiType::Anthropic => {
            Box::new(anthropic::Client::new(spec).await?) as Box<dyn LlmGenerationClient>
        }
        LlmApiType::LiteLlm => {
            Box::new(litellm::Client::new_litellm(spec).await?) as Box<dyn LlmGenerationClient>
        }
        LlmApiType::OpenRouter => {
            Box::new(openrouter::Client::new_openrouter(spec).await?) as Box<dyn LlmGenerationClient>
        }


    };
    Ok(client)
}
