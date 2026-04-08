import gradio as gr
from models import Action

def create_gradio_app(env):
    def reset_env(difficulty):
        obs = env.reset(task_difficulty=difficulty)
        return obs.code, obs.status, f"Score: {env.reward_state.score}"

    def step_env(action_type, description):
        try:
            action = Action(action_type=action_type, description=description)
            resp = env.step(action)
            obs = resp.observation
            done_text = "Yes" if resp.done else "No"
            return obs.code, obs.status, f"Score: {resp.info['score']} | Done: {done_text}"
        except Exception as e:
            return str(e), "Error", "Error"

    with gr.Blocks(title="Code Review Simulation") as demo:
        gr.Markdown("# OpenEnv Code Review Simulation Environment")
        
        with gr.Row():
            with gr.Column():
                difficulty = gr.Radio(["easy", "medium", "hard"], label="Difficulty", value="medium")
                reset_btn = gr.Button("Reset Environment")
                
                code_view = gr.Code(label="PR Code Snippet", language="python")
                status_view = gr.Textbox(label="PR Status")
                score_view = gr.Textbox(label="Current Reward Score")
                
            with gr.Column():
                gr.Markdown("### Agent Actions")
                action_type = gr.Dropdown(
                    choices=["detect_issue", "suggest_fix", "approve_pr", "reject_pr"], 
                    label="Action Type"
                )
                action_desc = gr.Textbox(label="Action Description (Analysis/Fix)")
                step_btn = gr.Button("Take Step")
                
        reset_btn.click(reset_env, inputs=[difficulty], outputs=[code_view, status_view, score_view])
        step_btn.click(step_env, inputs=[action_type, action_desc], outputs=[code_view, status_view, score_view])
        
    return demo
