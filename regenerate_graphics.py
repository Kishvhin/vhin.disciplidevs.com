#!/usr/bin/env python3
"""
Regenerate graphics with new enhanced design
"""
import json
from pathlib import Path
from graphics.graphic_generator import GraphicGenerator

def main():
    # Initialize generator
    generator = GraphicGenerator()
    
    # Get all approved content
    approved_dir = Path("data/approved_content")
    approved_files = list(approved_dir.glob("approved_*.json"))
    
    print(f"\n🎨 Regenerating {len(approved_files)} graphics with new design...\n")
    
    success_count = 0
    for filepath in approved_files:
        try:
            # Load report
            with open(filepath, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            print(f"📸 Creating graphic for: {report['headline'][:60]}...")
            
            # Generate new graphic
            graphic_path = generator.create_graphic(report)
            
            if graphic_path:
                print(f"   ✅ Saved to: {graphic_path}")
                success_count += 1
            else:
                print(f"   ❌ Failed to create graphic")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✨ Done! Successfully created {success_count}/{len(approved_files)} graphics")
    print(f"\n📁 View graphics at: data/graphics/")
    print(f"🌐 Or view in dashboard: http://localhost:5000/graphics\n")

if __name__ == "__main__":
    main()

