"""
Social Media Graphic Generator for NDTA
Creates branded graphics for social media posts with background images
"""
import logging
from pathlib import Path
from typing import Dict, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap
import requests
from io import BytesIO
import random

log = logging.getLogger(__name__)


class GraphicGenerator:
    """Generates NDTA-branded social media graphics with background images"""

    def __init__(self):
        self.output_dir = Path("data/graphics")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir = Path("graphics/templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir = Path("data/image_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Default dimensions (optimized for social media - Instagram/Facebook)
        self.width = 1080
        self.height = 1080

        # NDTA Brand Colors (matching your examples)
        self.colors = {
            'primary': '#003366',      # Dark blue (NDTA blue)
            'secondary': '#FDB913',    # Gold/Yellow (NDTA accent)
            'accent': '#FFFFFF',       # White
            'text': '#003366',         # Dark blue text
            'background': '#F5F5F5',   # Light gray
            'overlay': '#FFFFFF'       # White overlay
        }

        # Unsplash API (free tier - no key needed for basic usage)
        self.unsplash_base = "https://source.unsplash.com"

        # Image search keywords based on content
        self.image_keywords = {
            'construction': ['construction-site', 'construction-worker', 'building-construction'],
            'dump_truck': ['dump-truck', 'construction-vehicle', 'heavy-equipment'],
            'infrastructure': ['highway-construction', 'road-construction', 'infrastructure'],
            'equipment': ['excavator', 'construction-equipment', 'heavy-machinery'],
            'safety': ['construction-safety', 'safety-equipment', 'construction-worker'],
            'default': ['construction-site', 'dump-truck', 'construction']
        }
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_background_image(self, report: Dict) -> Optional[Image.Image]:
        """Download relevant background image from multiple sources"""
        try:
            # Determine image category based on content
            headline = report.get('headline', '').lower()
            summary = report.get('executive_summary', '').lower()
            content = headline + ' ' + summary

            # Select appropriate keywords
            keywords = self.image_keywords['default']
            if 'dump truck' in content or 'dumper' in content:
                keywords = self.image_keywords['dump_truck']
            elif 'safety' in content or 'accident' in content:
                keywords = self.image_keywords['safety']
            elif 'equipment' in content or 'machinery' in content:
                keywords = self.image_keywords['equipment']
            elif 'infrastructure' in content or 'highway' in content or 'road' in content:
                keywords = self.image_keywords['infrastructure']
            elif 'construction' in content:
                keywords = self.image_keywords['construction']

            # Pick random keyword for variety
            keyword = random.choice(keywords)

            # Try multiple image sources
            sources = [
                # Picsum (Lorem Picsum) - reliable, no API key needed
                f"https://picsum.photos/{self.width}/{self.height}",
                # Unsplash (backup)
                f"{self.unsplash_base}/{self.width}x{self.height}/?{keyword}",
            ]

            for url in sources:
                try:
                    log.info(f"Downloading background image from: {url[:50]}...")
                    response = requests.get(url, timeout=10, allow_redirects=True)

                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        log.info(f"✅ Successfully downloaded background image")
                        return img
                    else:
                        log.warning(f"Failed to download from this source: {response.status_code}")
                        continue

                except Exception as e:
                    log.warning(f"Error with this source: {e}")
                    continue

            # If all sources fail, create a gradient background
            log.warning("All image sources failed, creating gradient background")
            return self.create_gradient_background()

        except Exception as e:
            log.error(f"Error downloading background image: {e}")
            return self.create_gradient_background()

    def create_gradient_background(self) -> Image.Image:
        """Create a blue gradient background as fallback"""
        img = Image.new('RGB', (self.width, self.height), self.hex_to_rgb('#003366'))
        draw = ImageDraw.Draw(img)

        # Create vertical gradient from dark blue to lighter blue
        for y in range(self.height):
            # Calculate color for this row
            ratio = y / self.height
            r = int(0 + (100 * ratio))
            g = int(51 + (150 * ratio))
            b = int(102 + (200 * ratio))

            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        return img

    def create_overlay(self, width: int, height: int, opacity: float = 0.7) -> Image.Image:
        """Create a semi-transparent white overlay"""
        overlay = Image.new('RGBA', (width, height), (255, 255, 255, int(255 * opacity)))
        return overlay
    
    def create_graphic(self, report: Dict) -> Optional[Path]:
        """Create a professional social media graphic with background image"""

        log.info(f"Creating graphic for: {report['headline']}")

        try:
            # Download background image
            background = self.get_background_image(report)

            if background:
                # Use downloaded image as background
                img = background.resize((self.width, self.height), Image.Resampling.LANCZOS)

                # Apply slight blur to background for better text readability
                img = img.filter(ImageFilter.GaussianBlur(radius=2))

                # Darken the image slightly
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(0.7)

            else:
                # Fallback to solid color background
                img = Image.new('RGB', (self.width, self.height),
                              self.hex_to_rgb(self.colors['background']))

            # Convert to RGBA for overlay
            img = img.convert('RGBA')

            # Create white overlay for bottom section (like your examples)
            overlay_height = 450
            overlay = Image.new('RGBA', (self.width, overlay_height), (255, 255, 255, 240))
            img.paste(overlay, (0, self.height - overlay_height), overlay)

            # Convert back to RGB for drawing
            img = img.convert('RGB')
            draw = ImageDraw.Draw(img)

            # Load fonts
            try:
                # Try to load Arial (Windows) or fallback fonts
                logo_font = ImageFont.truetype("arialbd.ttf", 45)  # Bold for NDTA
                headline_font = ImageFont.truetype("arialbd.ttf", 65)  # Large bold headline
                subtext_font = ImageFont.truetype("arial.ttf", 32)
                footer_font = ImageFont.truetype("arial.ttf", 28)
            except:
                try:
                    logo_font = ImageFont.truetype("arial.ttf", 45)
                    headline_font = ImageFont.truetype("arial.ttf", 65)
                    subtext_font = ImageFont.truetype("arial.ttf", 32)
                    footer_font = ImageFont.truetype("arial.ttf", 28)
                except:
                    # Ultimate fallback
                    logo_font = ImageFont.load_default()
                    headline_font = ImageFont.load_default()
                    subtext_font = ImageFont.load_default()
                    footer_font = ImageFont.load_default()

            # Draw NDTA logo/text at top of white section
            logo_y = self.height - overlay_height + 30

            # NDTA text in blue
            draw.text(
                (50, logo_y),
                "NDTA",
                fill=self.hex_to_rgb(self.colors['primary']),
                font=logo_font
            )

            # Yellow underline accent (like your examples)
            draw.rectangle(
                [(50, logo_y + 55), (180, logo_y + 65)],
                fill=self.hex_to_rgb(self.colors['secondary'])
            )

            # Extract key number/stat from headline if present (like "$32M", "$48M")
            headline = report['headline']
            key_stat = None

            # Look for dollar amounts or percentages
            import re
            money_match = re.search(r'\$[\d.]+[MBK]?', headline)
            percent_match = re.search(r'\d+%', headline)

            if money_match:
                key_stat = money_match.group()
                headline = headline.replace(key_stat, '').strip()
            elif percent_match:
                key_stat = percent_match.group()
                headline = headline.replace(key_stat, '').strip()

            # Draw key stat in large yellow text (if found)
            stat_y = logo_y + 90
            if key_stat:
                draw.text(
                    (50, stat_y),
                    key_stat,
                    fill=self.hex_to_rgb(self.colors['secondary']),
                    font=headline_font
                )
                stat_y += 80

            # Draw headline (wrapped, in blue)
            wrapped_headline = textwrap.fill(headline, width=28)
            headline_lines = wrapped_headline.split('\n')[:2]  # Max 2 lines

            y_position = stat_y
            for line in headline_lines:
                draw.text(
                    (50, y_position),
                    line,
                    fill=self.hex_to_rgb(self.colors['primary']),
                    font=subtext_font
                )
                y_position += 45

            # Add state badge if state-specific (like your examples)
            if report.get('is_state_specific') and report.get('detected_states'):
                state = report['detected_states'][0]
                badge_text = f"📍 {state['name']}"

                y_position += 10
                draw.text(
                    (50, y_position),
                    badge_text,
                    fill=self.hex_to_rgb(self.colors['text']),
                    font=footer_font
                )

            # Add footer with website
            footer_y = self.height - 50
            draw.text(
                (50, footer_y),
                "www.thendta.org",
                fill=self.hex_to_rgb(self.colors['primary']),
                font=footer_font
            )

            # Save image
            filename = f"graphic_{report['id']}.png"
            filepath = self.output_dir / filename
            img.save(filepath, 'PNG', quality=95)

            # Update report with graphic path
            report['graphic_path'] = str(filepath)
            report['status'] = 'pending_approval'

            # Save updated report
            from content_generator.report_generator import ReportGenerator
            gen = ReportGenerator()
            gen.save_report(report)

            log.info(f"Graphic created: {filepath}")
            return filepath

        except Exception as e:
            log.error(f"Error creating graphic: {e}", exc_info=True)
            return None
    
    def create_state_specific_graphic(self, report: Dict, state: Dict) -> Optional[Path]:
        """Create a state-specific graphic with background image"""

        log.info(f"Creating state-specific graphic for {state['name']}")

        try:
            # Use the same process as regular graphic
            # The state badge will be added automatically
            return self.create_graphic(report)

        except Exception as e:
            log.error(f"Error creating state graphic: {e}", exc_info=True)
            return None

