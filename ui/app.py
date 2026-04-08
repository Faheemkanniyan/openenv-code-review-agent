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

    def run_agent(custom_code, language):
        from inference import InferenceAgent
        agent = InferenceAgent()
        logs, suggested_fix = agent.run_episode(custom_code=custom_code, language=language)
        return logs, suggested_fix

    with gr.Blocks(title="Code Review Simulation", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# OpenEnv Code Review Simulation")
        
        with gr.Tabs() as tabs:
            with gr.TabItem("Simulation View"):
                # Simulation View logic remains same
                with gr.Row():
                    with gr.Column(scale=1):
                        difficulty = gr.Radio(["easy", "medium", "hard"], label="Difficulty", value="medium")
                        reset_btn = gr.Button("Reset Environment", variant="secondary")
                        status_view = gr.Textbox(label="PR Status", interactive=False)
                        score_view = gr.Textbox(label="Current Reward Score", interactive=False)
                    with gr.Column(scale=2):
                        code_view = gr.Code(label="PR Code Snippet", language="python", interactive=False)
                    with gr.Column(scale=1):
                        gr.Markdown("### Manual Agent Actions")
                        action_type = gr.Dropdown(choices=["detect_issue", "suggest_fix", "approve_pr", "reject_pr"], label="Action Type")
                        action_desc = gr.Textbox(label="Action Description (Analysis/Fix)", placeholder="Enter your reasoning...")
                        step_btn = gr.Button("Take Step", variant="primary")
                        
                reset_btn.click(reset_env, inputs=[difficulty], outputs=[code_view, status_view, score_view])
                step_btn.click(step_env, inputs=[action_type, action_desc], outputs=[code_view, status_view, score_view])

            with gr.TabItem("Custom Code Analysis"):
                with gr.Row():
                    with gr.Column(scale=1):
                        language_select = gr.Dropdown(
                            choices=["python", "javascript", "cpp", "java", "csharp", "go", "rust"],
                            label="Programming Language",
                            value="python"
                        )
                        custom_code_input = gr.Code(label="Input Your Code", language="python", lines=15)
                        analyze_btn = gr.Button("Analyze with AI Agent", variant="primary")
                        
                    with gr.Column(scale=1):
                        with gr.Tabs():
                            with gr.TabItem("Analysis Report"):
                                analysis_output = gr.Markdown(label="Agent Analysis Logs")
                            with gr.TabItem("Suggested Fixes"):
                                fix_output = gr.Code(label="Suggested Fix Code", language="python", interactive=False)
                
                analyze_btn.click(
                    run_agent, 
                    inputs=[custom_code_input, language_select], 
                    outputs=[analysis_output, fix_output]
                )





        
    return demo
