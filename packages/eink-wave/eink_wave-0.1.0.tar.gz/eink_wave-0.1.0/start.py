#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
4.2 inch E-Paper Display Demo Script
This script demonstrates various features of the 4.2 inch e-ink display
including text rendering, graphics drawing, image display, and 4-gray mode.
"""

import os
import logging
import time
import traceback
from PIL import Image, ImageDraw, ImageFont

# Import the e-paper display module
from waveshare_epd.epd4in2_V2 import EPD

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EPaperDisplay:
    def __init__(self):
        """Initialize the e-paper display"""
        self.epd = None
        self.font24 = None
        self.font18 = None
        self.font35 = None
        
    def initialize(self):
        """Initialize the display and load fonts"""
        try:
            logging.info("Initializing 4.2 inch E-Paper Display...")
            self.epd = EPD()
            self.epd.init()
            self.epd.Clear()
            
            # Load system fonts
            self.font24 = ImageFont.load_default()
            self.font18 = ImageFont.load_default()
            self.font35 = ImageFont.load_default()
            
            logging.info("Display initialized successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize display: {e}")
            return False
    
    def display_text_demo(self):
        """Display text and basic graphics demo"""
        try:
            logging.info("Displaying text and graphics demo...")
            
            # Create horizontal image
            Himage = Image.new('1', (self.epd.width, self.epd.height), 255)
            draw = ImageDraw.Draw(Himage)
            
            # Add text
            draw.text((10, 0), 'Hello World!', font=self.font24, fill=0)
            draw.text((10, 30), '4.2 inch E-Paper Display', font=self.font24, fill=0)
            draw.text((10, 60), 'Raspberry Pi / Jetson Nano', font=self.font18, fill=0)
            draw.text((10, 90), 'Waveshare Electronics', font=self.font18, fill=0)
            
            # Add some graphics
            draw.line((20, 120, 70, 170), fill=0, width=2)
            draw.line((70, 120, 20, 170), fill=0, width=2)
            draw.rectangle((20, 120, 70, 170), outline=0, width=2)
            
            draw.line((165, 120, 165, 170), fill=0, width=2)
            draw.line((140, 145, 190, 145), fill=0, width=2)
            draw.arc((140, 120, 190, 170), 0, 360, fill=0)
            
            draw.rectangle((80, 120, 130, 170), fill=0)
            draw.chord((200, 120, 250, 170), 0, 360, fill=0)
            
            # Display the image
            self.epd.display(self.epd.getbuffer(Himage))
            time.sleep(3)
            
            logging.info("Text demo completed")
            
        except Exception as e:
            logging.error(f"Error in text demo: {e}")
    
    def display_4gray_demo(self):
        """Display 4-gray mode demo"""
        try:
            logging.info("Displaying 4-gray mode demo...")
            
            # Initialize 4-gray mode
            self.epd.Init_4Gray()
            
            # Create 4-gray image
            Limage = Image.new('L', (self.epd.width, self.epd.height), 0)
            draw = ImageDraw.Draw(Limage)
            
            # Add text with different gray levels
            draw.text((20, 0), '4-Gray Mode Demo', font=self.font35, fill=self.epd.GRAY1)
            draw.text((20, 40), 'Light Gray Text', font=self.font24, fill=self.epd.GRAY2)
            draw.text((20, 70), 'Medium Gray Text', font=self.font24, fill=self.epd.GRAY3)
            draw.text((20, 100), 'Dark Gray Text', font=self.font24, fill=0)
            
            # Add some graphics
            draw.line((10, 140, 60, 190), fill=self.epd.GRAY1, width=3)
            draw.rectangle((10, 140, 60, 190), outline=self.epd.GRAY2, width=2)
            draw.arc((70, 140, 120, 190), 0, 360, fill=self.epd.GRAY3)
            
            # Display the 4-gray image
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(Limage))
            time.sleep(3)
            
            logging.info("4-gray demo completed")
                
        except Exception as e:
            logging.error(f"Error in 4-gray demo: {e}")
    
    def display_info_screen(self):
        """Display system information screen"""
        try:
            logging.info("Displaying system information...")
            
            Himage = Image.new('1', (self.epd.width, self.epd.height), 255)
            draw = ImageDraw.Draw(Himage)
            
            # Add system information
            draw.text((10, 10), 'System Information', font=self.font35, fill=0)
            draw.text((10, 60), 'Display: 4.2 inch E-Paper', font=self.font18, fill=0)
            draw.text((10, 85), 'Resolution: 400x300', font=self.font18, fill=0)
            draw.text((10, 110), 'Interface: SPI', font=self.font18, fill=0)
            draw.text((10, 135), 'Driver: Waveshare EPD', font=self.font18, fill=0)
            
            # Add timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            draw.text((10, 180), f'Time: {timestamp}', font=self.font18, fill=0)
            
            # Add status
            draw.text((10, 220), 'Status: Ready', font=self.font24, fill=0)
            
            self.epd.display(self.epd.getbuffer(Himage))
            time.sleep(3)
            
        except Exception as e:
            logging.error(f"Error in info screen: {e}")
    
    def clear_display(self):
        """Clear the display"""
        try:
            logging.info("Clearing display...")
            self.epd.Clear()
        except Exception as e:
            logging.error(f"Error clearing display: {e}")
    
    def sleep_display(self):
        """Put display to sleep"""
        try:
            logging.info("Putting display to sleep...")
            self.epd.sleep()
        except Exception as e:
            logging.error(f"Error putting display to sleep: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.epd:
                self.clear_display()
                self.sleep_display()
            logging.info("Cleanup completed")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    def display_snake_demo(self):
        """Display an animated snake game on the display"""
        try:
            logging.info("Displaying animated snake demo...")
            
            # Snake game parameters
            snake = [(10, 10)]  # Start position
            direction = (1, 0)  # Start moving right
            food = (20, 10)     # Initial food position
            snake_length = 1

            Himage = Image.new('1', (self.epd.width, self.epd.height), 255)
            draw = ImageDraw.Draw(Himage)
            self.epd.display(self.epd.getbuffer(Himage))

            import code
            code.interact(local=dict(globals(), **locals()))

            draw.rectangle((0, 0, 10, 10), fill=0)
            draw.rectangle((10, 10, 20, 20), fill=0)
            self.epd.display(self.epd.getbuffer(Himage))

            # Game loop
            for frame in range(50):  # Run for 50 frames
                # Create white background
                Himage = Image.new('1', (self.epd.width, self.epd.height), 255)
                draw = ImageDraw.Draw(Himage)
                
                # Move snake head
                new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
                
                # Wrap around screen edges
                new_head = (new_head[0] % self.epd.width, new_head[1] % self.epd.height)
                
                # Check if snake ate food
                if new_head == food:
                    snake_length += 1
                    # Generate new food position
                    food = ((food[0] + 15) % self.epd.width, (food[1] + 10) % self.epd.height)
                
                # Add new head
                snake.insert(0, new_head)
                
                # Keep snake at current length
                if len(snake) > snake_length:
                    snake.pop()
                
                # Check if snake ate itself
                if new_head in snake[1:]:
                    logging.info("Snake ate itself! Game over.")
                    break
                
                # Change direction occasionally to create zigzag pattern
                if frame % 10 == 0:
                    if direction == (1, 0):  # Moving right
                        direction = (0, 1)   # Move down
                    elif direction == (0, 1):  # Moving down
                        direction = (-1, 0)  # Move left
                    elif direction == (-1, 0): # Moving left
                        direction = (0, -1)  # Move up
                    else:  # Moving up
                        direction = (1, 0)   # Move right
                
                # Draw snake
                for segment in snake:
                    draw.rectangle([segment[0], segment[1], segment[0]+2, segment[1]+2], fill=0)
                
                # Draw food
                draw.rectangle([food[0], food[1], food[0]+2, food[1]+2], fill=0)
                
                # Display the image
                self.epd.display(self.epd.getbuffer(Himage))
                time.sleep(0.5)  # Faster animation
                
                logging.info(f"Frame {frame}: Snake length = {snake_length}")
            
            logging.info("Snake demo completed")
            
        except Exception as e:
            logging.error(f"Error in snake demo: {e}")

    def display_partial_animation_demo(self):
        """Display an animation of drawing small boxes around the perimeter using partial updates"""
        try:
            logging.info("Displaying partial update animation demo...")
            
            # Create a base white image
            base_image = Image.new('1', (self.epd.width, self.epd.height), 255)
            base_buffer = self.epd.getbuffer(base_image)
            
            # Box size for the animation
            box_size = 8
            
            # Define the perimeter positions (clockwise around the screen)
            perimeter_positions = []
            
            # Top edge (left to right)
            for x in range(0, self.epd.width - box_size, box_size * 2):
                perimeter_positions.append((x, 0))
            
            # Right edge (top to bottom)
            for y in range(0, self.epd.height - box_size, box_size * 2):
                perimeter_positions.append((self.epd.width - box_size, y))
            
            # Bottom edge (right to left)
            for x in range(self.epd.width - box_size, 0, -box_size * 2):
                perimeter_positions.append((x, self.epd.height - box_size))
            
            # Left edge (bottom to top)
            for y in range(self.epd.height - box_size, 0, -box_size * 2):
                perimeter_positions.append((0, y))
            
            # Create the animation
            current_image = Image.new('1', (self.epd.width, self.epd.height), 255)
            draw = ImageDraw.Draw(current_image)
            
            # Display initial white screen
            self.epd.display_Partial(base_buffer)
            time.sleep(1)
            
            # Animate drawing boxes around the perimeter
            for i, (x, y) in enumerate(perimeter_positions):
                # Draw a black box at the current position
                draw.rectangle([x, y, x + box_size, y + box_size], fill=0)
                
                # Add text in the center showing the current index
                text = str(i + 1)
                # Calculate center position for text
                text_bbox = draw.textbbox((0, 0), text, font=self.font24)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = (self.epd.width - text_width) // 2
                text_y = (self.epd.height - text_height) // 2
                
                # Clear previous text area (draw white rectangle)
                draw.rectangle([text_x - 5, text_y - 5, text_x + text_width + 5, text_y + text_height + 5], fill=255)
                
                # Draw the new text
                draw.text((text_x, text_y), text, font=self.font24, fill=0)
                
                # Get the updated buffer
                current_buffer = self.epd.getbuffer(current_image)
                
                # Update the display using partial refresh
                self.epd.display_Partial(current_buffer)
                
                # Small delay to see the animation
                time.sleep(0.1)
                
                logging.info(f"Drawing box {i+1}/{len(perimeter_positions)} at position ({x}, {y})")
            
            # Pause to show the completed perimeter
            time.sleep(2)
            
            # Now animate removing the boxes (drawing white boxes)
            for i, (x, y) in enumerate(perimeter_positions):
                # Draw a white box to "erase" the black box
                draw.rectangle([x, y, x + box_size, y + box_size], fill=255)
                
                # Update text in the center showing the removal index
                text = f"R{i + 1}"  # R for "removing"
                # Calculate center position for text
                text_bbox = draw.textbbox((0, 0), text, font=self.font24)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = (self.epd.width - text_width) // 2
                text_y = (self.epd.height - text_height) // 2
                
                # Clear previous text area (draw white rectangle)
                draw.rectangle([text_x - 5, text_y - 5, text_x + text_width + 5, text_y + text_height + 5], fill=255)
                
                # Draw the new text
                draw.text((text_x, text_y), text, font=self.font24, fill=0)
                
                # Get the updated buffer
                current_buffer = self.epd.getbuffer(current_image)
                
                # Update the display using partial refresh
                self.epd.display_Partial(current_buffer)
                
                # Small delay to see the animation
                time.sleep(0.1)
                
                logging.info(f"Removing box {i+1}/{len(perimeter_positions)} at position ({x}, {y})")
            
            # Final pause
            time.sleep(1)
            
            logging.info("Partial update animation completed")
            
        except Exception as e:
            logging.error(f"Error in partial update animation: {e}")
            traceback.print_exc()

def main():
    """Main function to run the e-paper display demo"""
    display = EPaperDisplay()
    
    try:
        # Initialize the display
        if not display.initialize():
            logging.error("Failed to initialize display. Exiting.")
            return
        
        logging.info("Starting 4.2 inch E-Paper Display Demo")
        
        # Comment out most of the original demos
        # display.display_text_demo()
        # display.display_4gray_demo()
        # display.display_info_screen()
        
        # Run the new partial update animation demo
        display.display_partial_animation_demo()
        
        # Final clear and sleep
        display.clear_display()
        display.sleep_display()
        
        logging.info("Demo completed successfully!")
        
    except KeyboardInterrupt:
        logging.info("Demo interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        traceback.print_exc()
    finally:
        display.cleanup()

if __name__ == "__main__":
    main()
