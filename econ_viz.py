"""
Economic Concept Visualizer
A system for meta-categorizing and visualizing economic concepts with standardized graphics.

Usage:
    python econ_visualizer.py

Requirements:
    pip install matplotlib numpy
"""

from dataclasses import dataclass, field
from typing import List, Dict, Literal, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Agent:
    """Represents an economic agent (person, firm, country, etc.)"""
    type: Literal["individual", "firm", "institution", "country", "market"]
    id: str
    count: int = 1
    position: Tuple[float, float] = (0, 0)
    color: str = "tan"
    label: Optional[str] = None


@dataclass
class Good:
    """Represents a product or resource"""
    type: str
    count: int
    position: Tuple[float, float]
    color: str = "white"
    size: float = 0.3


@dataclass
class Flow:
    """Represents exchange or information flow between agents"""
    from_pos: Tuple[float, float]
    to_pos: Tuple[float, float]
    label: str = ""
    thickness: float = 2.0
    color: str = "white"


@dataclass
class Label:
    """Glassmorphism-style text label"""
    text: str
    position: Tuple[float, float]
    fontsize: int = 11
    style: Literal["normal", "title", "subtitle"] = "normal"


@dataclass
class TimeStep:
    """Complete state at a specific time"""
    t: int
    agents: List[Agent] = field(default_factory=list)
    goods: List[Good] = field(default_factory=list)
    flows: List[Flow] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)


@dataclass
class MetaCategories:
    """Meta-categorization framework for economic concepts"""
    agent_types: List[str]
    scale_level: Literal["micro", "meso", "macro", "multi-level"]
    interaction_pattern: Literal["isolated", "bilateral", "oligopolistic", 
                                  "competitive", "hierarchical", "network", "market-mediated"]
    information_structure: Literal["perfect", "imperfect", "asymmetric", "signaling", "learning"]
    time_structure: Literal["static", "sequential", "dynamic", "stochastic"]
    decision_scope: List[str]
    equilibrium_concept: Optional[str] = None


@dataclass
class EconomicConcept:
    """Complete economic concept with meta-categorization and visualization"""
    name: str
    description: str
    meta: MetaCategories
    time_steps: List[TimeStep]
    wiki_url: Optional[str] = None


# ============================================================================
# VISUALIZER
# ============================================================================

class EconVisualizer:
    """Renders economic concepts as clean overhead visualizations"""
    
    def __init__(self, figsize=(14, 10)):
        self.figsize = figsize
        self.fig = None
        self.ax = None
        
    def setup_canvas(self):
        """Initialize clean canvas"""
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-8, 8)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.fig.patch.set_facecolor('white')
        
    def draw_agent(self, agent: Agent):
        """Draw economic agent as geometric shape"""
        x, y = agent.position
        
        if agent.type in ["country", "firm", "institution", "market"]:
            # Rectangle for structural agents
            width = 2.0 if agent.type == "country" else 1.5
            height = 1.6 if agent.type == "country" else 1.2
            
            rect = mpatches.Rectangle(
                (x - width/2, y - height/2), width, height,
                facecolor=agent.color,
                edgecolor='#333',
                linewidth=1.5,
                alpha=0.85
            )
            self.ax.add_patch(rect)
            
            # Add agent label if provided
            if agent.label:
                self.ax.text(x, y, agent.label, 
                           fontsize=9, ha='center', va='center',
                           fontfamily='sans-serif', weight='bold',
                           color='#333')
                
        elif agent.type == "individual":
            # Circle for individuals
            circle = mpatches.Circle(
                (x, y), 0.25,
                facecolor=agent.color,
                edgecolor='#333',
                linewidth=1
            )
            self.ax.add_patch(circle)
    
    def draw_good(self, good: Good):
        """Draw goods/products as small boxes"""
        x, y = good.position
        size = good.size
        
        rect = mpatches.Rectangle(
            (x - size/2, y - size/2), size, size,
            facecolor=good.color,
            edgecolor='#333',
            linewidth=0.8,
            alpha=0.9
        )
        self.ax.add_patch(rect)
    
    def draw_flow(self, flow: Flow):
        """Draw arrow showing exchange/flow"""
        self.ax.annotate(
            '',
            xy=flow.to_pos,
            xytext=flow.from_pos,
            arrowprops=dict(
                arrowstyle='->',
                lw=flow.thickness,
                color=flow.color,
                alpha=0.9,
                connectionstyle="arc3,rad=0"
            )
        )
        
        # Label on arrow if provided
        if flow.label:
            mid_x = (flow.from_pos[0] + flow.to_pos[0]) / 2
            mid_y = (flow.from_pos[1] + flow.to_pos[1]) / 2
            self.draw_label(Label(flow.label, (mid_x, mid_y + 0.3), fontsize=9))
    
    def draw_label(self, label: Label):
        """Draw glassmorphism-style label"""
        x, y = label.position
        
        # Style variations
        if label.style == "title":
            fontsize = 16
            weight = 'bold'
            alpha = 0.8
        elif label.style == "subtitle":
            fontsize = 13
            weight = 'semibold'
            alpha = 0.75
        else:
            fontsize = label.fontsize
            weight = 'normal'
            alpha = 0.7
        
        # Glassmorphism box
        bbox = dict(
            boxstyle='round,pad=0.5',
            facecolor='white',
            alpha=alpha,
            edgecolor='#ccc',
            linewidth=0.8
        )
        
        self.ax.text(
            x, y, label.text,
            fontsize=fontsize,
            ha='center',
            va='center',
            bbox=bbox,
            fontfamily='sans-serif',
            weight=weight,
            color='#333'
        )
    
    def render_timestep(self, concept: EconomicConcept, timestep_idx: int = 0):
        """Render complete timestep visualization"""
        self.setup_canvas()
        
        timestep = concept.time_steps[timestep_idx]
        
        # Draw all components
        for agent in timestep.agents:
            self.draw_agent(agent)
        
        for good in timestep.goods:
            self.draw_good(good)
        
        for flow in timestep.flows:
            self.draw_flow(flow)
        
        for label in timestep.labels:
            self.draw_label(label)
        
        # Add title
        self.ax.text(0, 7.5, f"{concept.name} (t={timestep.t})",
                    fontsize=18, ha='center', weight='bold',
                    fontfamily='sans-serif', color='#222')
        
        plt.tight_layout()
    
    def save(self, filename: str, dpi: int = 300):
        """Save current visualization"""
        plt.savefig(filename, dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✓ Saved: {filename}")
    
    def show(self):
        """Display visualization"""
        plt.show()


# ============================================================================
# CONCEPT LIBRARY
# ============================================================================

def create_absolute_advantage() -> EconomicConcept:
    """
    Absolute Advantage: One country can produce goods more efficiently than another.
    https://en.wikipedia.org/wiki/Absolute_advantage
    """
    
    meta = MetaCategories(
        agent_types=["country"],
        scale_level="macro",
        interaction_pattern="bilateral",
        information_structure="perfect",
        time_structure="sequential",
        decision_scope=["production", "trade"],
        equilibrium_concept="comparative advantage equilibrium"
    )
    
    # t=0: No trade (autarky)
    t0 = TimeStep(
        t=0,
        agents=[
            Agent("country", "A", position=(-5, 0), color="tan"),
            Agent("country", "B", position=(5, 0), color="tan"),
        ],
        goods=[
            # Country A: 10 cloth, 6 wine
            *[Good("cloth", 1, (-6 + i*0.35, -2.5), "white", 0.25) for i in range(10)],
            *[Good("wine", 1, (-5.5 + i*0.45, -3.5), "#8B4513", 0.25) for i in range(6)],
            # Country B: 4 cloth, 2 wine
            *[Good("cloth", 1, (4.5 + i*0.35, -2.5), "white", 0.25) for i in range(4)],
            *[Good("wine", 1, (5 + i*0.45, -3.5), "#8B4513", 0.25) for i in range(2)],
        ],
        labels=[
            Label("COUNTRY A", (-5, 1.5), style="subtitle"),
            Label("10 cloth, 6 wine", (-5, -4.5)),
            Label("COUNTRY B", (5, 1.5), style="subtitle"),
            Label("4 cloth, 2 wine", (5, -4.5)),
            Label("NO TRADE | TOTAL: 14 cloth, 8 wine", (0, -6.5), fontsize=12, style="subtitle")
        ]
    )
    
    # t=1: With specialization and trade
    t1 = TimeStep(
        t=1,
        agents=[
            Agent("country", "A", position=(-5, 0), color="tan"),
            Agent("country", "B", position=(5, 0), color="tan"),
        ],
        goods=[
            # Country A: specialized in cloth (20 total)
            *[Good("cloth", 1, (-7 + (i%10)*0.35, -2.5 + (i//10)*0.35), "white", 0.25) for i in range(20)],
            # Country B: specialized in wine (4 total)
            *[Good("wine", 1, (4.5 + i*0.45, -2.5), "#8B4513", 0.25) for i in range(4)],
        ],
        flows=[
            Flow((-3, 0), (3, 0), "8 cloth →", 2.5, "#4A90E2"),
            Flow((3, -1), (-3, -1), "← 2 wine", 2.5, "#E94B3C"),
        ],
        labels=[
            Label("COUNTRY A", (-5, 1.5), style="subtitle"),
            Label("Produces: 20 cloth", (-5, -4), fontsize=10),
            Label("Keeps: 12 cloth + 2 wine", (-5, -4.8), fontsize=9),
            Label("COUNTRY B", (5, 1.5), style="subtitle"),
            Label("Produces: 4 wine", (5, -4), fontsize=10),
            Label("Keeps: 8 cloth + 2 wine", (5, -4.8), fontsize=9),
            Label("TRADE", (0, 0.8), fontsize=10),
            Label("SPECIALIZATION | Total: 20 cloth, 4 wine | Both better off", 
                  (0, -6.5), fontsize=11, style="subtitle")
        ]
    )
    
    return EconomicConcept(
        name="Absolute Advantage",
        description="One country can produce all goods more efficiently, but trade still benefits both through specialization",
        meta=meta,
        time_steps=[t0, t1],
        wiki_url="https://en.wikipedia.org/wiki/Absolute_advantage"
    )


def create_market_equilibrium() -> EconomicConcept:
    """
    Market Equilibrium: Price adjusts until quantity supplied equals quantity demanded.
    https://en.wikipedia.org/wiki/Economic_equilibrium
    """
    
    meta = MetaCategories(
        agent_types=["individual", "firm"],
        scale_level="micro",
        interaction_pattern="market-mediated",
        information_structure="perfect",
        time_structure="dynamic",
        decision_scope=["consumption", "production", "pricing"],
        equilibrium_concept="partial equilibrium"
    )
    
    # t=0: Price too high, surplus
    t0 = TimeStep(
        t=0,
        agents=[
            # Sellers (left)
            Agent("individual", "S1", position=(-3, 2), color="#7FB3D5"),
            Agent("individual", "S2", position=(-3, 0), color="#7FB3D5"),
            Agent("individual", "S3", position=(-3, -2), color="#7FB3D5"),
            # Buyers (right) - fewer because price is high
            Agent("individual", "B1", position=(3, 0), color="#F1948A"),
        ],
        flows=[
            # Only one transaction happening
            Flow((-1, 0), (1, 0), "", 2.0, "#52BE80"),
        ],
        labels=[
            Label("SUPPLY: 3 units", (-3, 3.5), fontsize=11, style="subtitle"),
            Label("DEMAND: 1 unit", (3, 3.5), fontsize=11, style="subtitle"),
            Label("PRICE = $10 (TOO HIGH)", (0, -3.5), fontsize=12, style="subtitle"),
            Label("SURPLUS: 2 unsold", (0, -5), fontsize=11),
        ]
    )
    
    # t=1: Equilibrium price
    t1 = TimeStep(
        t=1,
        agents=[
            # Sellers (fewer, one exited)
            Agent("individual", "S1", position=(-3, 1), color="#7FB3D5"),
            Agent("individual", "S2", position=(-3, -1), color="#7FB3D5"),
            # Buyers (more, one entered)
            Agent("individual", "B1", position=(3, 1), color="#F1948A"),
            Agent("individual", "B2", position=(3, -1), color="#F1948A"),
        ],
        flows=[
            # Two transactions
            Flow((-1, 1), (1, 1), "", 2.0, "#52BE80"),
            Flow((-1, -1), (1, -1), "", 2.0, "#52BE80"),
        ],
        labels=[
            Label("SUPPLY: 2 units", (-3, 3.5), fontsize=11, style="subtitle"),
            Label("DEMAND: 2 units", (3, 3.5), fontsize=11, style="subtitle"),
            Label("PRICE = $7 (EQUILIBRIUM)", (0, -3.5), fontsize=12, style="subtitle"),
            Label("SURPLUS: 0", (0, -5), fontsize=11),
        ]
    )
    
    return EconomicConcept(
        name="Market Equilibrium",
        description="Price adjusts until quantity supplied equals quantity demanded",
        meta=meta,
        time_steps=[t0, t1],
        wiki_url="https://en.wikipedia.org/wiki/Economic_equilibrium"
    )


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Generate visualizations for economic concepts"""
    
    print("Economic Concept Visualizer")
    print("=" * 50)
    print()
    
    # Initialize visualizer
    viz = EconVisualizer()
    
    # Generate Absolute Advantage
    print("Generating: Absolute Advantage")
    concept = create_absolute_advantage()
    
    viz.render_timestep(concept, timestep_idx=0)
    viz.save("absolute_advantage_t0.png")
    
    viz.render_timestep(concept, timestep_idx=1)
    viz.save("absolute_advantage_t1.png")
    print()
    
    # Generate Market Equilibrium
    print("Generating: Market Equilibrium")
    concept = create_market_equilibrium()
    
    viz.render_timestep(concept, timestep_idx=0)
    viz.save("market_equilibrium_t0.png")
    
    viz.render_timestep(concept, timestep_idx=1)
    viz.save("market_equilibrium_t1.png")
    print()
    
    print("=" * 50)
    print("✓ All visualizations generated successfully!")
    print("\nTo view: Check the generated PNG files")
    print("To add concepts: Add new create_*() functions following the pattern")


if __name__ == "__main__":
    main()
