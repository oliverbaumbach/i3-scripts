"""
Utility functions for i3 blocks formatting 


"""

################################################################################


def _to_sRGB(component):
    """
    Convert linear Color to sRGB 
    """
    component = 12.92 * component if component <= 0.0031308 else (1.055 * (component**(1/2.4))) - 0.055
    return int(255.9999 * component)

def _from_sRGB(component):
    """
    Linearize sRGB color 
    """
    component /= 255.0
    return component / 12.92 if component <= 0.04045 else ((component+0.055)/1.055)**2.4

def _from_Hex(color):
    """
    Converts #RRGGBB hex code into (r,g,b) tuple 
    """
    color = color.lstrip('#')
    return [int(color[i:i+2], 16) for i in range(0, 6, 2)]

def _to_Hex(color):
    """
    Converts (r,g,b) tuple into #RRGGBB hex code 
    """
    return "".join(f"{component:02x}" for component in color)

def gradient_at(gradient, mix, gamma=0.43):
    """
    Calculates color at specified point in gradient. 

    Parameters
    ----------- 
    gradient : list
       list of (<hex code>, <stop>) tuples sorted by stop 
    mix : float 
       position on the gradient 

    Returns 
    -------
    tuple  
       (r,g,b)-tuple containing color at point 
    """
    # Get first two tuples (<hex code1>, <stop1>), (<hex_code2>, <stop2>) where stop2 > mix 
    color1, color2 = next((a,b) for a,b in           
                          (gradient[i:i+2] for i           
                           in range(len(gradient)-1))
                          if b[1] >= mix)  
    color1, stop1 = color1
    color2, stop2 = color2
    
    # Scale mix to interval [stop1, stop2]
    mix = (mix - stop1) / (stop2 - stop1)

    # Convert both colors from hex codes to (r,g,b)-tuples 
    color1 = _from_Hex(color1)
    color2 = _from_Hex(color2)

    # Convert both colors to linear representation 
    color1 = [_from_sRGB(component) for component in color1]
    color2 = [_from_sRGB(component) for component in color2]

    # Calculate color brightnesses 
    bright1 = sum(color1)**gamma
    bright2 = sum(color2)**gamma

    # Interpolate Colors
    lerp = lambda a,b,t: a*(1-t) + b*t
    intensity = lerp(bright1, bright2, mix)**(1/gamma)
    color = [lerp(component1, component2, mix) for
             component1, component2 in
             zip(color1, color2)]
    if sum(color) != 0:
        color = tuple((component * intensity / sum(color)) for component in color)
    # Return hex code for color 
    return _to_Hex(_to_sRGB(component) for component in color)

def span(text, font=None, fg=None, bg=None):
    """
    Generate pango formatting span around text 
    """
    return ("<span" +
            (f" font='{font}'" if font else "") +
            (f" foreground='#{fg}'" if fg else "") +
            (f" background='#{bg}'" if bg else "") +
            f">{text}</span>")

def fa(codepoint):
    """
    Generate formatting for Font Awesome Icond 
    """
    return f"<span font='Font Awesome Heavy'>&#x{codepoint};</span>"
 
