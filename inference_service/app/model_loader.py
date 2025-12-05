"""
Mistral 7B model loader and inference handler
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from typing import Optional
import logging

from .config import settings

logger = logging.getLogger(__name__)


class MistralModel:
    """Mistral 7B model wrapper"""
    
    def __init__(self):
        self.model: Optional[AutoModelForCausalLM] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.device = settings.DEVICE
        self.model_name = settings.MODEL_NAME
        
    def load(self):
        """Load the Mistral 7B model and tokenizer"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            logger.info(f"Device: {self.device}")
            
            # Configure quantization if requested
            quantization_config = None
            if settings.LOAD_IN_4BIT:
                logger.info("Loading model in 4-bit mode")
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
            elif settings.LOAD_IN_8BIT:
                logger.info("Loading model in 8-bit mode")
                quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            model_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            }
            
            if quantization_config:
                model_kwargs["quantization_config"] = quantization_config
                model_kwargs["device_map"] = "auto"
            else:
                model_kwargs["device_map"] = self.device
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs
            )
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 1.0
    ) -> str:
        """
        Generate text completion
        
        Args:
            prompt: Input text prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated text
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        try:
            # Enforce token limits
            max_new_tokens = min(max_new_tokens, settings.MAX_OUTPUT_TOKENS)
            
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=settings.MAX_INPUT_TOKENS,
                truncation=True
            ).to(self.device if not settings.LOAD_IN_4BIT and not settings.LOAD_IN_8BIT else "cuda")
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True if temperature > 0 else False,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode output (excluding input prompt)
            generated_text = self.tokenizer.decode(
                outputs[0][inputs.input_ids.shape[1]:],
                skip_special_tokens=True
            )
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if not self.tokenizer:
            raise RuntimeError("Tokenizer not loaded")
        return len(self.tokenizer.encode(text))
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.tokenizer is not None


# Global model instance
mistral_model = MistralModel()
