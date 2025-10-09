import json
from typing import List, Dict, Any


class DialogueConverter:
    """Convert tab-separated dialogue data to text and JSON formats."""
    
    def __init__(self):
        self.dialogues = []
        self.current_dialogue = []
    
    def parse_line(self, line: str) -> Dict[str, Any]:
        """Parse a single tab-separated line."""
        parts = line.strip().split('\t')
        
        if len(parts) < 3:
            return None
        
        speaker = parts[0].strip()
        text = parts[1].strip()
        intent = parts[2].strip()
        scores = parts[3].strip() if len(parts) > 3 else ""
        
        # Parse scores
        score_list = []
        if scores:
            score_list = [int(s.strip()) for s in scores.split(',') if s.strip()]
        
        return {
            "speaker": speaker,
            "text": text,
            "intent": intent,
            "scores": score_list if score_list else None
        }
    
    def read_from_file(self, filename: str):
        """Read dialogue data from a file."""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self._process_lines(lines)
    
    def read_from_text(self, text: str):
        """Read dialogue data from a string."""
        lines = text.strip().split('\n')
        self._process_lines(lines)
    
    def _process_lines(self, lines: List[str]):
        """Process lines and split into dialogues."""
        for line in lines:
            if not line.strip():
                continue
            
            parsed = self.parse_line(line)
            if not parsed:
                continue
            
            # Check if this is the OVERALL marker (end of dialogue)
            if parsed["speaker"] == "USER" and parsed["text"] == "OVERALL":
                if self.current_dialogue:
                    self.dialogues.append({
                        "turns": self.current_dialogue,
                        "overall_scores": parsed["scores"]
                    })
                    self.current_dialogue = []
            else:
                self.current_dialogue.append(parsed)
        
        # Add the last dialogue if exists and no OVERALL was found
        if self.current_dialogue:
            self.dialogues.append({
                "turns": self.current_dialogue,
                "overall_scores": None
            })
    
    def calculate_dialogue_average(self, dialogue: Dict) -> float:
        """Calculate average score for a dialogue (using overall_scores if available)."""
        if dialogue["overall_scores"]:
            return sum(dialogue["overall_scores"]) / len(dialogue["overall_scores"])
        
        # Fallback: average all turn scores if no overall scores
        all_scores = []
        for turn in dialogue["turns"]:
            if turn["scores"]:
                all_scores.extend(turn["scores"])
        
        return sum(all_scores) / len(all_scores) if all_scores else 0.0
    
    def scale_score(self, score, old_min=1, old_max=5, new_min=1, new_max=100):
        # To prevent division by zero, if the old range is a single number,
        # return the minimum of the new range.
        if (old_max - old_min) == 0:
            return new_min
        
        # Apply the linear scaling formula
        new_score = (
            new_min + (score - old_min) * (new_max - new_min) / (old_max - old_min)
        )
        
        return new_score
    
    def to_text_format(self, output_file: str):
        """Convert to text format with DIALOGUE 1, DIALOGUE 2, etc."""
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, dialogue in enumerate(self.dialogues, 1):
                avg_score = self.calculate_dialogue_average(dialogue)
                
                f.write(f"DIALOGUE {idx} (Average Score: {avg_score:.2f})\n")
                f.write("=" * 80 + "\n\n")
                
                for turn in dialogue["turns"]:
                    f.write(f"{turn['speaker']}: {turn['text']}\n")
                    if turn['scores']:
                        f.write(f"[Intent: {turn['intent']} | Scores: {','.join(map(str, turn['scores']))}]\n")
                    else:
                        f.write(f"[Intent: {turn['intent']}]\n")
                    f.write("\n")
                
                if dialogue["overall_scores"]:
                    f.write(f"OVERALL SCORES: {','.join(map(str, dialogue['overall_scores']))} (Average: {avg_score:.2f})\n")
                
                f.write("\n" + "=" * 80 + "\n\n")
        
        print(f"✓ Text format saved to {output_file}")
        print(f"  Total dialogues: {len(self.dialogues)}")
    
    def to_json_format(self, output_file: str, pretty: bool = True):
        """Convert to JSON format."""
        json_data = {
            "total_dialogues": len(self.dialogues),
            "dialogues": []
        }
        
        for idx, dialogue in enumerate(self.dialogues, 1):
            avg_score = self.calculate_dialogue_average(dialogue)
            
            dialogue_data = {
                "dialogue_id": idx,
                "turns": [],
                "overall_scores": dialogue["overall_scores"],
                "average_score": round(avg_score, 2),
                "average_score_100": round(self.scale_score(avg_score), 2) if avg_score > 0 else None     
                
            }
            
            turn_id = 1
            for turn in dialogue["turns"]:
                turn_data = {
                    "turn_id": turn_id,
                    "speaker": turn["speaker"],
                    "text": turn["text"],
                    "intent": turn["intent"],
                    "scores": turn["scores"]
                }
                dialogue_data["turns"].append(turn_data)
                turn_id += 1
            
            json_data["dialogues"].append(dialogue_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(json_data, f, ensure_ascii=False)
        
        print(f"✓ JSON format saved to {output_file}")
        print(f"  Total dialogues: {len(self.dialogues)}")
    
    def to_chat_format_json(self, output_file: str):
        """Convert to chat-style JSON format (role: user/assistant)."""
        json_data = {"conversations": []}
        
        for idx, dialogue in enumerate(self.dialogues, 1):
            avg_score = self.calculate_dialogue_average(dialogue)
            
            conversation = {
                "conversation_id": idx,
                "messages": [],
                "overall_scores": dialogue["overall_scores"],
                "average_score": round(avg_score, 2),
                "average_score_100": round(self.scale_score(avg_score), 2) if avg_score > 0 else None   
            }
            
            for turn in dialogue["turns"]:
                role = "user" if turn["speaker"] == "USER" else "assistant"
                message = {
                    "role": role,
                    "content": turn["text"]
                }
                
                # Add metadata if present
                if turn["intent"] != "OTHER" or turn["scores"]:
                    message["metadata"] = {
                        "intent": turn["intent"],
                        "scores": turn["scores"]
                    }
                
                conversation["messages"].append(message)
            
            json_data["conversations"].append(conversation)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Chat format JSON saved to {output_file}")
        print(f"  Total conversations: {len(self.dialogues)}")
    
    def get_statistics(self):
        """Get statistics about the dialogues."""
        total_turns = sum(len(d["turns"]) for d in self.dialogues)
        avg_turns = total_turns / len(self.dialogues) if self.dialogues else 0
        
        intent_counts = {}
        for dialogue in self.dialogues:
            for turn in dialogue["turns"]:
                intent = turn["intent"]
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        # Calculate average scores for all dialogues
        dialogue_scores = []
        for dialogue in self.dialogues:
            avg_score = self.calculate_dialogue_average(dialogue)
            dialogue_scores.append(avg_score)
        
        overall_avg = sum(dialogue_scores) / len(dialogue_scores) if dialogue_scores else 0
        
        return {
            "total_dialogues": len(self.dialogues),
            "total_turns": total_turns,
            "average_turns_per_dialogue": round(avg_turns, 2),
            "intent_distribution": intent_counts,
            "dialogue_average_scores": dialogue_scores,
            "overall_average_score": round(overall_avg, 2),
            "overall_average_score_100": round(self.scale_score(overall_avg), 2) if overall_avg > 0 else None
        }
    
    def print_statistics(self):
        """Print statistics about the dialogues."""
        stats = self.get_statistics()
        print("\n" + "=" * 50)
        print("DIALOGUE STATISTICS")
        print("=" * 50)
        print(f"Total Dialogues: {stats['total_dialogues']}")
        print(f"Total Turns: {stats['total_turns']}")
        print(f"Average Turns per Dialogue: {stats['average_turns_per_dialogue']}")
        print(f"\nOverall Average Score: {stats['overall_average_score']}")
        print("\nIndividual Dialogue Scores:")
        for idx, score in enumerate(stats['dialogue_average_scores'], 1):
            print(f"  Dialogue {idx}: {score:.2f}")
        print("\nIntent Distribution:")
        for intent, count in sorted(stats['intent_distribution'].items(), key=lambda x: -x[1]):
            print(f"  {intent}: {count}")
        print("=" * 50 + "\n")


# Example usage
if __name__ == "__main__":
    # Create converter
    converter = DialogueConverter()
    input_path = 'data'
    output_path = 'output'
    
    # Read from your file
    converter.read_from_file(f'{input_path}/CCPE.txt')
    
    # Print statistics
    converter.print_statistics()
    
    # Convert to different formats
    converter.to_text_format(f'{output_path}/dialogues_output.txt')
    converter.to_json_format(f'{output_path}/dialogues_output.json')
    converter.to_chat_format_json(f'{output_path}/dialogues_chat_format.json')

    print("\n✓ All conversions completed successfully!")
    print("\nGenerated files:")
    print("  1. dialogues_output.txt - Human-readable text format")
    print("  2. dialogues_output.json - Structured JSON format")
    print("  3. dialogues_chat_format.json - Chat-style format for LLMs")