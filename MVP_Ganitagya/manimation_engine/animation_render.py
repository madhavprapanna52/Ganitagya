import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

def create_and_render_video(script, quality='high', output_dir=None):
    """
    Create and render a mathematical video using Manim, returning the path to the generated video.
    
    Args:
        script (dict): Dictionary containing:
            - 'text_definition': String with the mathematical concept definition
            - 'equation': String with the mathematical equation (e.g., "x**2 + 2*x + 1")
            - 'title': Optional title for the video
            - 'variable': Optional variable name (default: 'x')
        quality (str): Video quality - 'high', 'medium', 'low' (default: 'high')
        output_dir (str): Optional custom output directory for the final video
    
    Returns:
        str: Absolute path to the generated video file, or None if rendering failed
    """
    
    # Your provided Manim code (embedded as a string to write to temp file)
    manim_code = '''from manim import *
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

# Set the script data
set_script(SCRIPT_DATA)
'''
    
    try:
        # Create a temporary directory for the Manim script
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create the script file
            script_file = os.path.join(temp_dir, "math_video_generator.py")
            
            # Replace SCRIPT_DATA placeholder with actual script
            script_code = manim_code.replace('SCRIPT_DATA', repr(script))
            
            # Write the script to file
            with open(script_file, 'w') as f:
                f.write(script_code)
            
            # Determine quality flag
            quality_flags = {
                'high': '-pqh',
                'medium': '-pqm', 
                'low': '-pql'
            }
            quality_flag = quality_flags.get(quality.lower(), '-pqh')
            
            # Prepare the manim command
            cmd = [
                sys.executable, '-m', 'manim',
                script_file,
                'MathVideoScene',
                quality_flag
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            print("Rendering video... This may take a few minutes.")
            
            # Run manim command
            result = subprocess.run(
                cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print("✅ Video rendered successfully!")
                
                # Determine the expected output path based on quality
                quality_dirs = {
                    '-pqh': '1080p60',
                    '-pqm': '720p30', 
                    '-pql': '480p15'
                }
                quality_dir = quality_dirs.get(quality_flag, '1080p60')
                
                # Find the generated video file
                media_path = os.path.join(temp_dir, 'media', 'videos', 'math_video_generator', quality_dir, 'MathVideoScene.mp4')
                
                if os.path.exists(media_path):
                    # Create final output directory
                    if output_dir is None:
                        output_dir = os.path.join(os.getcwd(), 'generated_videos')
                    
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Generate a unique filename based on the script
                    safe_title = "".join(c for c in script.get('title', 'math_video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    safe_title = safe_title.replace(' ', '_')
                    final_filename = f"{safe_title}_{quality}.mp4"
                    final_path = os.path.join(output_dir, final_filename)
                    
                    # Copy the video to the final location
                    shutil.copy2(media_path, final_path)
                    
                    print(f"✅ Video saved to: {os.path.abspath(final_path)}")
                    return os.path.abspath(final_path)
                else:
                    print(f"❌ Video file not found at expected location: {media_path}")
                    print("Available files:")
                    for root, dirs, files in os.walk(os.path.join(temp_dir, 'media')):
                        for file in files:
                            print(f"  - {os.path.join(root, file)}")
                    return None
            else:
                print(f"❌ Manim rendering failed with return code: {result.returncode}")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return None
                
    except subprocess.TimeoutExpired:
        print("❌ Video rendering timed out (>5 minutes)")
        return None
    except Exception as e:
        print(f"❌ Error during video generation: {str(e)}")
        return None

def generate_and_save_video(script, quality='high', output_dir=None):
    """
    Convenience function that combines your generate_video function concept 
    with automatic rendering and path return.
    
    Args:
        script (dict): Same as create_and_render_video
        quality (str): 'high', 'medium', or 'low'
        output_dir (str): Optional output directory
    
    Returns:
        str: Path to the generated video file, or None if failed
    """
    return create_and_render_video(script, quality, output_dir)

# Example usage
if __name__ == "__main__":
    # Test the function
    test_script = {
        'title': 'Test Quadratic Function',
        'text_definition': 'A quadratic function is a polynomial function of degree 2. It forms a parabola when graphed.',
        'equation': 'x**2 + 2*x + 1',
        'variable': 'x'
    }
    
    print("Testing video generation...")
    video_path = create_and_render_video(test_script, quality='low')  # Use low quality for faster testing
    
    if video_path:
        print(f"SUCCESS! Video generated at: {video_path}")
    else:
        print("FAILED to generate video")
