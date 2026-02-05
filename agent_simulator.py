import os
import json
import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------
# ⚙️ CONFIGURATION
# ------------------------------------------------------------------
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# 🚨 CONTROL FLAGS
# True = Call API & Save Images. 
# False = Print Prompts Only.
GENERATE = False 

# 🚨 MODEL SETTINGS
LLM_MODEL = "gpt-5.2"          
IMAGE_MODEL = "gpt-image-1.5"  

# ------------------------------------------------------------------
# 🎨 AGENT LOGIC
# ------------------------------------------------------------------

class EconomicStoryboardAgent:
    def __init__(self):
        # ----------------------------------------------------------
        # 1. THE "REALISM + CLARITY" DNA 
        # ----------------------------------------------------------
        self.entity_style_dna = """
        Visual Style: High-fidelity, photorealistic miniature simulation.
        
        CRITICAL COMPOSITION RULES (Anti-Clutter):
        - DISTINCT GROUPS: Do not clump agents/objects together. Use negative space to separate different elements.
        - SILHOUETTES: Every object must have a clear, readable outline.
        - ZONING: Organize the scene into clear 'zones' (e.g., Production Zone vs. Shipping Zone) rather than a chaotic mix.
        - DEPTH: Use depth of field to keep the main action in sharp focus.
        
        Content Rules:
        - NO METAPHORS (No magic, scales, monsters, balloons).
        - SHOW THE MECHANISM (Price tags, inventory piles, idle machinery, shipping queues).
        - INFRASTRUCTURE: Use realistic industry assets (conveyor belts, server racks, shipping containers).
        - ACTORS: Realistic tiny humans in appropriate attire.
        """
        
        # ----------------------------------------------------------
        # 2. THE "TECH-GLASS" BASE
        # ----------------------------------------------------------
        self.stage_settings = """
        Stage Design:
        - Base: A wafer-thin, translucent frosted-glass platform (acrylic style).
        - Edges: Smooth, rounded corners with a soft neon blue/teal edge emission.
        - Environment: Pitch black void. The only light comes from the scene and the base glow.
        - Perspective: Isometric orthographic.
        """

    def plan_scenes(self, concept):
        print(f"🎬 Director ({LLM_MODEL}): Planning extended simulation for '{concept}'...")
        
        prompt = f"""
        You are a Realistic Economic Simulator.
        Goal: Visualize the concept "{concept}" using ONLY literal, physical economic activities.
        
        INSTRUCTIONS:
        1. Analyze the complexity of the concept.
        2. Break it down into a chronological sequence of simulation states.
        3. DYNAMIC LENGTH: Use between 2 to 6 scenes. Do not rush. If the concept needs 5 steps to show the cause-and-effect properly, use 5 steps.
        
        STRICT VISUAL RULES:
        - NO VISUAL METAPHORS.
        - SHOW CAUSE & EFFECT (e.g., Step 1: Factory running; Step 2: Supply shortage; Step 3: Production halts).
        
        Return JSON ONLY: 
        {{ "scenes": [ 
            {{ 
                "step": 1, 
                "title": "State 1 Title", 
                "sector": "Industry Type", 
                "visual_action": "Detailed description emphasizing distinct object separation." 
            }} 
        ] }}
        """
        
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL, 
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content).get("scenes", [])
        except Exception as e:
            print(f"❌ Planning Error: {e}")
            return []

    def generate_prompt(self, scene_data):
        return f"""
        A photorealistic 3D isometric simulation of {scene_data['sector']}.
        
        SCENE ACTION (Literal Economic Mechanism):
        {scene_data['visual_action']}
        
        {self.entity_style_dna}
        {self.stage_settings}
        
        Details:
        - Step {scene_data.get('step', 1)}: {scene_data.get('title')}.
        - Ensure high contrast between objects and the background for readability.
        """

    def render_storyboard(self, concept):
        scenes = self.plan_scenes(concept)
        if not scenes: return

        print(f"📋 Simulation Plan: {len(scenes)} states defined.")
        
        for scene in scenes:
            print(f"\n👉 Processing Step {scene['step']}: {scene['title']}...")
            prompt = self.generate_prompt(scene)
            filename = f"{concept.replace(' ', '_')}_step{scene['step']}.png"
            
            # --------------------------------------------------
            # 🛑 DRY RUN MODE
            # --------------------------------------------------
            if not GENERATE:
                print("\n" + "="*60)
                print(f"📝 PROMPT FOR STEP {scene['step']} (COPY BELOW):")
                print("-" * 20)
                print(prompt.strip())
                print("-" * 20)
                print("="*60 + "\n")
                continue 

            # --------------------------------------------------
            # 🎨 GENERATE MODE
            # --------------------------------------------------
            try:
                print(f"   🎨 Sending to {IMAGE_MODEL}...")
                
                response = client.images.generate(
                    model=IMAGE_MODEL,
                    prompt=prompt,
                    size="1024x1024",
                    n=1
                )
                
                # 🕵️ DATA EXTRACTION
                image_data = None
                data_obj = response.data[0]

                if getattr(data_obj, 'url', None):
                    image_data = requests.get(data_obj.url).content
                elif getattr(data_obj, 'b64_json', None):
                    image_data = base64.b64decode(data_obj.b64_json)
                elif isinstance(data_obj, dict):
                     if 'url' in data_obj: image_data = requests.get(data_obj['url']).content
                     elif 'b64_json' in data_obj: image_data = base64.b64decode(data_obj['b64_json'])

                if image_data:
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                    print(f"   ✅ Simulation Captured: {filename}")
                else:
                    print(f"   ❌ Error: No image data found.")

            except Exception as e:
                print(f"   ❌ Simulation Failed: {e}")

if __name__ == "__main__":
    agent = EconomicStoryboardAgent()
    
    # Test with a complex concept to trigger multiple steps
    concept = "the Fisher equation, which expresses the relationship between nominal interest rates, real interest rates, and inflation" 
    
    agent.render_storyboard(concept)