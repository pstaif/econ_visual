import os
import json
import requests
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------
# ⚙️ CONFIGURATION
# ------------------------------------------------------------------
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# 🚨 MODEL SETTINGS
LLM_MODEL = "gpt-5.2"          
IMAGE_MODEL = "gpt-image-1.5"  

# ------------------------------------------------------------------
# 🎨 AGENT LOGIC
# ------------------------------------------------------------------

class EconomicStoryboardAgent:
    def __init__(self):
        self.entity_style_dna = """
        Visual Style: Minimalist 3D isometric, institutional design.
        Material: Realistic steel/concrete machinery sitting on the glass base.
        Lighting: Cinematic studio lighting with soft reflections on the floor.
        """
        
        # ----------------------------------------------------------
        # 💎 NEW BASE STYLE: "Glassmorphism / Tech-Neon"
        # ----------------------------------------------------------
        self.stage_settings = """
        View: Isometric orthographic projection.
        
        Base: A thin, translucent frosted-glass platform (acrylic). 
        - Shape: A sleek, rounded rectangle with smooth beveled edges.
        - Glow: Soft neon blue/teal emission on the edges only.
        - Thickness: Very slim/wafer-thin floating profile.
        
        Background: Pitch black void to make the neon edges pop.
        Grid: Faint, laser-etched white grid lines on the glass surface.
        """        


        """ original
        self.entity_style_dna =
        Visual Style: Minimalist 3D isometric, institutional/civic design.
        Material: Realistic steel/concrete, not cartoonish.
        Lighting: Cinematic studio lighting.
        
        self.stage_settings =
        View: Isometric orthographic.
        Base: Rounded concrete base on black background.
        Grid: Faint slanted grid on floor.
        """
       

    def plan_scenes(self, concept):
        print(f"🎬 Director ({LLM_MODEL}): Planning '{concept}'...")
        prompt = f"""
        Analyze "{concept}". Break into 1-3 scenes.
        Return JSON ONLY: {{ "scenes": [ {{ "step": 1, "title": "Title", "sector": "Sector", "visual_action": "Action" }} ] }}
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
        Isometric icon of {scene_data['sector']}.
        Action: {scene_data['visual_action']}.
        {self.entity_style_dna}
        {self.stage_settings}
        """

    def render_storyboard(self, concept):
        scenes = self.plan_scenes(concept)
        if not scenes: return

        print(f"📋 Plan approved: {len(scenes)} scenes.")
        
        for scene in scenes:
            print(f"\n🎨 Rendering Step {scene['step']} using {IMAGE_MODEL}...")
            prompt = self.generate_prompt(scene)
            filename = f"{concept.replace(' ', '_')}_step{scene['step']}.png"
            
            try:
                # --------------------------------------------------
                # 🛡️ SAFE BARE-BONES REQUEST
                # --------------------------------------------------
                response = client.images.generate(
                    model=IMAGE_MODEL,
                    prompt=prompt,
                    size="1024x1024",
                    n=1
                    # NO style, NO quality, NO response_format
                )
                
                # --------------------------------------------------
                # 🕵️ DATA EXTRACTION & DEBUGGING
                # --------------------------------------------------
                image_data = None
                data_obj = response.data[0]

                # Check 1: Standard URL
                if getattr(data_obj, 'url', None):
                    print("   ⬇️  Downloading from URL...")
                    image_data = requests.get(data_obj.url).content
                
                # Check 2: Base64 JSON
                elif getattr(data_obj, 'b64_json', None):
                    print("   🧩 Decoding Base64...")
                    image_data = base64.b64decode(data_obj.b64_json)
                
                # Check 3: Raw Dict (some custom models return dicts)
                elif isinstance(data_obj, dict):
                     if 'url' in data_obj:
                         image_data = requests.get(data_obj['url']).content
                     elif 'b64_json' in data_obj:
                         image_data = base64.b64decode(data_obj['b64_json'])

                # 🛑 FAILURE HANDLING
                if image_data:
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                    print(f"   ✅ Saved: {filename}")
                else:
                    print("   ❌ Error: Could not find image data in response.")
                    print(f"   ⚠️ DEBUG RAW RESPONSE: {data_obj}")

            except Exception as e:
                print(f"   ❌ API Request Failed: {e}")

if __name__ == "__main__":
    agent = EconomicStoryboardAgent()
    agent.render_storyboard("Fisher equation, which expresses the relationship between nominal interest rates, real interest rates, and inflation")