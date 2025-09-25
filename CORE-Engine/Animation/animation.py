from manim import *
import numpy as np
import sympy as sp
from sympy import symbols, diff, integrate, solve
import os
import json

# Global variable to store the script data
CURRENT_SCRIPT = {}

def set_script(script):
    """Set the global script that will be used by the Manim scene"""
    global CURRENT_SCRIPT
    CURRENT_SCRIPT = script

class MathVideoScene(Scene):
    """
    Main Manim scene class for generating mathematical videos without LaTeX.
    This version uses the Text object for all equation and text rendering.
    """
    
    def construct(self):
        # Get script from global variable
        script = CURRENT_SCRIPT
        
        # Extract script components with defaults
        text_definition = script.get('text_definition', '')
        equation_str = script.get('equation', 'x**2')
        title = script.get('title', 'Mathematical Function Analysis')
        variable = script.get('variable', 'x')
        
        # Scene sequence
        self.show_title(title)
        
        if text_definition:
            self.show_definition(text_definition)
        
        self.show_equation(equation_str, variable)
        self.plot_function(equation_str, variable)
        self.geometric_analysis(equation_str, variable)
        self.mathematical_analysis(equation_str, variable)
    
    def show_title(self, title_text):
        """Display animated title"""
        title = Text(title_text, font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
    
    def show_definition(self, definition_text):
        """Display and animate the definition"""
        # Split long text into multiple lines
        max_chars_per_line = 60
        words = definition_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) < max_chars_per_line:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        definition_title = Text("Definition", font_size=36, color=GREEN).to_edge(UP)
        self.play(Write(definition_title))
        
        text_objects = []
        for i, line in enumerate(lines):
            text_obj = Text(line, font_size=24).shift(UP * (1 - i * 0.6))
            text_objects.append(text_obj)
            self.play(Write(text_obj), run_time=1.5)
        
        self.wait(3)
        self.play(*[FadeOut(obj) for obj in text_objects], FadeOut(definition_title))
    
    def show_equation(self, equation_str, var):
        """Display and animate the equation using Text instead of MathTex"""
        try:
            # Convert string to sympy expression
            x = symbols(var)
            expr = sp.sympify(equation_str.replace('^', '**'))
            
            # Create a simple string representation
            equation_text = f"f({var}) = {str(expr)}"
            
            equation_title = Text("Function Equation", font_size=36, color=YELLOW).to_edge(UP)
            equation = Text(equation_text, font_size=48)
            
            self.play(Write(equation_title))
            self.play(Write(equation))
            self.wait(2)
            
            self.play(Indicate(equation), color=RED)
            self.wait(1)
            self.play(FadeOut(equation_title), FadeOut(equation))
            
        except Exception as e:
            # Fallback for simple display
            equation_title = Text("Function Equation", font_size=36, color=YELLOW).to_edge(UP)
            equation = Text(f"f({var}) = {equation_str}", font_size=48)
            self.play(Write(equation_title))
            self.play(Write(equation))
            self.wait(2)
            self.play(FadeOut(equation_title), FadeOut(equation))
    
    def plot_function(self, equation_str, var):
        """Create animated plot of the function"""
        try:
            # Setup axes
            axes = Axes(
                x_range=[-5, 5, 1],
                y_range=[-10, 10, 2],
                tips=False,
                axis_config={"include_numbers": True}
            )
            
            axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
            
            # Convert equation to function
            x = symbols(var)
            expr = sp.sympify(equation_str.replace('^', '**'))
            
            # Create function for plotting
            def func(x_val):
                try:
                    return float(expr.subs(x, x_val))
                except:
                    return 0
            
            # Create the graph
            graph = axes.plot(func, color=BLUE, x_range=[-5, 5])
            
            plot_title = Text("Function Plot", font_size=36, color=PURPLE).to_edge(UP)
            
            # Animate the plotting
            self.play(Write(plot_title))
            self.play(Create(axes), Write(axes_labels))
            self.play(Create(graph), run_time=3)
            
            # Add some points on the curve
            points = []
            for x_val in [-2, -1, 0, 1, 2]:
                y_val = func(x_val)
                if abs(y_val) < 10:  # Only show points within reasonable range
                    point = Dot(axes.coords_to_point(x_val, y_val), color=RED)
                    points.append(point)
                    self.play(Create(point), run_time=0.3)
            
            self.wait(2)
            self.play(FadeOut(plot_title), FadeOut(axes), FadeOut(axes_labels), 
                     FadeOut(graph), *[FadeOut(point) for point in points])
            
        except Exception as e:
            # Fallback: show a simple parabola
            axes = Axes(x_range=[-3, 3], y_range=[-2, 8])
            graph = axes.plot(lambda x: x**2, color=BLUE)
            plot_title = Text("Sample Function Plot", font_size=36, color=PURPLE).to_edge(UP)
            
            self.play(Write(plot_title))
            self.play(Create(axes), Create(graph))
            self.wait(2)
            self.play(FadeOut(plot_title), FadeOut(axes), FadeOut(graph))
    
    def geometric_analysis(self, equation_str, var):
        """Show geometric representations and properties"""
        geo_title = Text("Geometric Analysis", font_size=36, color=ORANGE).to_edge(UP)
        self.play(Write(geo_title))
        
        try:
            x = symbols(var)
            expr = sp.sympify(equation_str.replace('^', '**'))
            
            # Create axes for geometric analysis
            axes = Axes(
                x_range=[-4, 4, 1],
                y_range=[-5, 15, 2],
                tips=False,
                axis_config={"include_numbers": True, "font_size": 24}
            )
            
            def func(x_val):
                try:
                    return float(expr.subs(x, x_val))
                except:
                    return x_val**2
            
            graph = axes.plot(func, color=BLUE, x_range=[-4, 4])
            
            self.play(Create(axes))
            self.play(Create(graph))
            
            # Show tangent line at a point
            x_point = 1
            y_point = func(x_point)
            
            # Calculate derivative for slope
            try:
                derivative = diff(expr, x)
                slope = float(derivative.subs(x, x_point))
            except:
                slope = 2 * x_point  # Default for x^2
            
            # Create tangent line
            tangent_func = lambda x_val: slope * (x_val - x_point) + y_point
            tangent_line = axes.plot(tangent_func, color=RED, x_range=[x_point-1.5, x_point+1.5])
            
            point = Dot(axes.coords_to_point(x_point, y_point), color=GREEN, radius=0.08)
            
            self.play(Create(point))
            self.play(Create(tangent_line))
            
            # Add labels
            tangent_label = Text("Tangent Line", font_size=20, color=RED).next_to(tangent_line, UP)
            point_label = Text(f"({x_point}, {y_point:.2f})", font_size=18).next_to(point, UR)
            
            self.play(Write(tangent_label), Write(point_label))
            
            self.wait(3)
            self.play(FadeOut(axes), FadeOut(graph), FadeOut(tangent_line), 
                     FadeOut(point), FadeOut(tangent_label), FadeOut(point_label))
            
        except Exception as e:
            # Simple geometric representation
            simple_text = Text("Geometric properties depend on the specific function", 
                             font_size=24).shift(DOWN)
            self.play(Write(simple_text))
            self.wait(2)
            self.play(FadeOut(simple_text))
        
        self.play(FadeOut(geo_title))
    
    def mathematical_analysis(self, equation_str, var):
        """Show mathematical analysis (derivatives, integrals, etc.) using Text"""
        analysis_title = Text("Mathematical Analysis", font_size=36, color=TEAL).to_edge(UP)
        self.play(Write(analysis_title))
        
        try:
            x = symbols(var)
            expr = sp.sympify(equation_str.replace('^', '**'))
            
            # Calculate derivative
            derivative = diff(expr, x)
            derivative_text = f"f'({var}) = {str(derivative)}"
            
            # Calculate integral
            integral = integrate(expr, x)
            integral_text = f"Integral of f({var}) = {str(integral)} + C"
            
            # Show derivative
            deriv_title = Text("Derivative:", font_size=28, color=GREEN).shift(UP * 1.5 + LEFT * 3)
            deriv_eq = Text(derivative_text, font_size=36).next_to(deriv_title, RIGHT)
            
            self.play(Write(deriv_title))
            self.play(Write(deriv_eq))
            
            # Show integral
            integral_title = Text("Integral:", font_size=28, color=BLUE).shift(DOWN * 0.5 + LEFT * 3)
            integral_eq = Text(integral_text, font_size=36).next_to(integral_title, RIGHT)
            
            self.play(Write(integral_title))
            self.play(Write(integral_eq))
            
            # Find critical points
            try:
                critical_points = solve(derivative, x)
                if critical_points:
                    critical_text = f"Critical points: {[float(pt) for pt in critical_points if pt.is_real]}"
                    critical_label = Text(critical_text, font_size=24, color=PURPLE).shift(DOWN * 2)
                    self.play(Write(critical_label))
                    self.wait(2)
                    self.play(FadeOut(critical_label))
            except:
                pass
            
            self.wait(3)
            self.play(FadeOut(deriv_title), FadeOut(deriv_eq), 
                     FadeOut(integral_title), FadeOut(integral_eq))
            
        except Exception as e:
            # Fallback analysis
            fallback_text = Text("Mathematical analysis requires a valid equation", 
                                 font_size=24)
            self.play(Write(fallback_text))
            self.wait(2)
            self.play(FadeOut(fallback_text))
        
        self.play(FadeOut(analysis_title))
        
        # Final summary
        summary = Text("End of Mathematical Analysis", font_size=32, color=WHITE)
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary))

def generate_video(script):
    """
    Generate an educational video using Manim based on a script containing
    text definitions and equations.
    
    Args:
        script (dict): Dictionary containing:
            - 'text_definition': String with the mathematical concept definition
            - 'equation': String with the mathematical equation (e.g., "x**2 + 2*x + 1")
            - 'title': Optional title for the video
            - 'variable': Optional variable name (default: 'x')
    
    Returns:
        str: Instructions on how to render the video
    """
    
    # Set the script globally so the scene can access it
    set_script(script)
    
    # Create output directory
    output_dir = "math_videos"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save script to file for reference
    script_file = os.path.join(output_dir, "current_script.json")
    with open(script_file, 'w') as f:
        json.dump(script, f, indent=2)
    
    instructions = f"""
Video generation setup complete!

To render the video, run one of these commands in your terminal:

1. For high quality (recommended):
   manim {__file__} MathVideoScene -pqh

2. For medium quality (faster):
   manim {__file__} MathVideoScene -pqm

3. For low quality (fastest):
   manim {__file__} MathVideoScene -pql

4. To preview without saving:
   manim {__file__} MathVideoScene --preview

The video will be saved in the 'media' folder created by Manim.
Script details saved to: {script_file}

Current script:
- Title: {script.get('title', 'Mathematical Function Analysis')}
- Equation: {script.get('equation', 'x**2')}
- Variable: {script.get('variable', 'x')}
"""
    
    print(instructions)
    return instructions

# Example usage and testing
if __name__ == "__main__":
    # Example script for testing
    sample_script = {
        'title': 'Quadratic Function Analysis',
        'text_definition': 'A quadratic function is a polynomial function of degree 2. It has the general form f(x) = ax^2 + bx + c where a != 0. The graph of a quadratic function is a parabola that opens upward if a > 0 and downward if a < 0.',
        'equation': 'x**2 + 2*x + 1',
        'variable': 'x'
    }
    
    # Set up the video generation
    result = generate_video(sample_script)
    
    print("\n" + "="*60)
    print("READY TO RENDER!")
    print("The MathVideoScene class is now available for Manim to use.")
    print("="*60)
