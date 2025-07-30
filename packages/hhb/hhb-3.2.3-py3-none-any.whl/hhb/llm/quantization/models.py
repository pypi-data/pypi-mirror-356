from .base import HHBBaseAWQForCausalLM


class HHBQwenAWQForCausalLM(HHBBaseAWQForCausalLM):
    layer_type = "QWenBlock"
    max_seq_len_key = "seq_length"

    @staticmethod
    def get_model_layers(model):
        return model.transformer.h

    @staticmethod
    def get_act_for_scaling(module):
        return dict(is_scalable=False)

    @staticmethod
    def move_embed(model, device: str):
        model.transformer.wte = model.transformer.wte.to(device)
        model.transformer.rotary_emb = model.transformer.rotary_emb.to(device)

    @staticmethod
    def get_layers_for_scaling(module, input_feat, module_kwargs):
        layers = []

        # attention
        layers.append(
            dict(
                prev_op=module.ln_1,
                layers=[module.attn.c_attn],
                inp=input_feat["attn.c_attn"],
                module2inspect=module.attn,
                kwargs=module_kwargs,
            )
        )

        # mlp
        layers.append(
            dict(
                prev_op=module.ln_2,
                layers=[module.mlp.w2, module.mlp.w1],
                inp=input_feat["mlp.w2"],
                module2inspect=module.mlp,
            )
        )

        # linear 2
        layers.append(
            dict(
                prev_op=module.mlp.w1,
                layers=[module.mlp.c_proj],
                inp=input_feat["mlp.c_proj"],
            )
        )

        return layers


class HHBQwen2AWQForCausalLM(HHBBaseAWQForCausalLM):
    layer_type = "QWenBlock"
    max_seq_len_key = "seq_length"

    @staticmethod
    def get_model_layers(model):
        return model.transformer.h

    @staticmethod
    def get_act_for_scaling(module):
        return dict(is_scalable=False)

    @staticmethod
    def move_embed(model, device: str):
        model.transformer.wte = model.transformer.wte.to(device)
        model.transformer.rotary_emb = model.transformer.rotary_emb.to(device)

    @staticmethod
    def get_layers_for_scaling(module, input_feat, module_kwargs):
        layers = []

        # attention
        layers.append(
            dict(
                prev_op=module.ln_1,
                layers=[module.attn.c_attn],
                inp=input_feat["attn.c_attn"],
                module2inspect=module.attn,
                kwargs=module_kwargs,
            )
        )

        # mlp
        layers.append(
            dict(
                prev_op=module.ln_2,
                layers=[module.mlp.w2, module.mlp.w1],
                inp=input_feat["mlp.w2"],
                module2inspect=module.mlp,
            )
        )

        # linear 2
        layers.append(
            dict(
                prev_op=module.mlp.w1,
                layers=[module.mlp.c_proj],
                inp=input_feat["mlp.c_proj"],
            )
        )

        return layers


class HHBChatGLMAWQForCausalLM(HHBBaseAWQForCausalLM):
    layer_type = "ChatGLMModel"
    max_seq_len_key = "seq_length"

    @staticmethod
    def get_model_layers(model):
        return model.transformer.encoder.layers

    @staticmethod
    def get_act_for_scaling(module):
        return dict(is_scalable=False)

    @staticmethod
    def move_embed(model, device: str):
        model.transformer.embedding.word_embeddings = (
            model.transformer.embedding.word_embeddings.to(device)
        )
        model.transformer.rotary_pos_emb = model.transformer.rotary_pos_emb.to(device)

    @staticmethod
    def get_layers_for_scaling(module, input_feat, module_kwargs):
        layers = []

        # attention
        layers.append(
            dict(
                prev_op=module.input_layernorm,
                layers=[module.self_attention.query_key_value],
                inp=input_feat["self_attention.query_key_value"],
                module2inspect=module.self_attention,
                kwargs=module_kwargs,
            )
        )

        # mlp
        layers.append(
            dict(
                prev_op=module.post_attention_layernorm,
                layers=[module.mlp.dense_h_to_4h],
                inp=input_feat["mlp.dense_h_to_4h"],
                module2inspect=module.mlp,
                kwargs=module_kwargs,
            )
        )

        # linear 2
        layers.append(
            dict(
                prev_op=module.mlp.dense_h_to_4h,
                layers=[module.mlp.dense_4h_to_h],
                inp=input_feat["mlp.dense_4h_to_h"],
            )
        )
        return layers
