#!/usr/bin/env python3

"""
Simple JGT Trading System Orchestrator

This module orchestrates the complete JGT trading system without external dependencies
for immediate testing and background service use.
"""

import argparse
import subprocess
import time
from typing import List


class SimpleTradingOrchestrator:
    """Simple trading system orchestrator using existing JGT components."""
    
    def __init__(self, timeframe: str, instruments: List[str], 
                 quality_threshold: float = 8.0, demo: bool = True, test_mode: bool = False):
        self.timeframe = timeframe
        self.instruments = instruments
        self.quality_threshold = quality_threshold
        self.demo = demo
        self.test_mode = test_mode
        
        print(f"🚀 Simple JGT Trading Orchestrator Initialized")
        print(f"📊 Timeframe: {timeframe} | Instruments: {','.join(instruments)}")
        if test_mode:
            print("⚡ TEST MODE ENABLED")
    
    def run_enhanced_trading_analysis(self) -> bool:
        """Run enhanced trading CLI analysis."""
        try:
            instruments_str = ','.join(self.instruments)
            mode_flag = '--demo' if self.demo else '--real'
            
            cmd = [
                'enhancedtradingcli', 'auto', 
                '-i', instruments_str,
                mode_flag,
                '--quality-threshold', str(self.quality_threshold)
            ]
            
            print(f"🔍 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, text=True)
            
            if result.returncode == 0:
                print("✅ Enhanced trading analysis completed")
                return True
            else:
                print(f"❌ Analysis failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def generate_analysis_charts(self) -> bool:
        """Generate analysis charts for all instruments."""
        success_count = 0
        
        for instrument in self.instruments:
            try:
                print(f"📈 Generating chart for {instrument} {self.timeframe}")
                
                cmd = [
                    'jgtads', '-i', instrument, '-t', self.timeframe,
                    '--save_figure', 'charts/',
                    '--save_figure_as_timeframe'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Chart generated for {instrument}")
                    success_count += 1
                else:
                    print(f"⚠️  Chart generation failed for {instrument}: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Error generating chart for {instrument}: {e}")
        
        return success_count > 0
    
    def update_trailing_stops(self) -> bool:
        """Update trailing stops for active trades."""
        try:
            mode_flag = '--demo' if self.demo else '--real'
            
            # Refresh trade data
            cmd_refresh = ['jgtapp', 'fxtr', mode_flag]
            print("🔄 Refreshing trade data...")
            
            result = subprocess.run(cmd_refresh, capture_output=True, text=True)
            if result.returncode != 0:
                print("⚠️  No active trades found or trade data unavailable")
                return False
            
            print("✅ Trade data refreshed")
            
            # Update FDB-based trailing stops with Alligator fallback
            print("🐊 Updating FDB-based trailing stops with Alligator fallback...")
            cmd_stops = ['jgtapp', 'fxmvstopfdb', '-t', self.timeframe, '--lips', mode_flag]
            
            result = subprocess.run(cmd_stops, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ FDB trailing stops updated")
                return True
            else:
                print(f"⚠️  FDB trailing stops update failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating trailing stops: {e}")
            return False
    
    def process_timeframe_trigger(self) -> bool:
        """Process actions when timeframe is triggered."""
        print(f"🎯 Processing {self.timeframe} timeframe trigger...")
        
        if self.timeframe in ["H4", "H1", "D1"]:
            print("📈 PRIMARY MARKET ANALYSIS MODE")
            
            # Step 1: Enhanced trading analysis
            if not self.run_enhanced_trading_analysis():
                return False
            
            # Step 2: Generate analysis charts
            if not self.generate_analysis_charts():
                print("⚠️  Chart generation had issues but continuing...")
            
            return True
            
        elif self.timeframe in ["m15", "m5"]:
            print("🎯 TRADE MANAGEMENT MODE")
            
            # Enhanced trading analysis for trade management
            if not self.run_enhanced_trading_analysis():
                print("⚠️  Enhanced analysis failed, continuing with basic trade management...")
            
            # Update trailing stops
            self.update_trailing_stops()
            
            return True
            
        elif self.timeframe == "m1":
            print("⚡ RAPID MONITORING MODE")
            
            # Quick enhanced analysis
            return self.run_enhanced_trading_analysis()
        
        else:
            print(f"❌ Unsupported timeframe: {self.timeframe}")
            return False
    
    def run_single_cycle(self) -> bool:
        """Run a single trading cycle."""
        if self.test_mode:
            print(f"🔄 SIMULATION: {self.timeframe} timeframe reached")
            time.sleep(1)
        
        return self.run_enhanced_trading_analysis()
    
    def run_continuous(self, max_cycles: int = None) -> None:
        """Run continuous trading orchestration."""
        cycle_count = 0
        
        if self.test_mode:
            # In test mode, just run once or a few cycles
            max_cycles = max_cycles or 1
            print(f"🧪 Test mode: Running {max_cycles} cycle(s)")
            
            for i in range(max_cycles):
                print(f"\n--- Test Cycle {i+1}/{max_cycles} ---")
                self.run_single_cycle()
                if i < max_cycles - 1:
                    time.sleep(2)  # Short delay between test cycles
            
            print("🎯 Test cycles completed")
            return
        
        # Real-time mode - single execution (called by timeframe scheduler)
        self.run_single_cycle()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Simple JGT Trading System Orchestrator",
        epilog="Example: python simple_trading_orchestrator.py --timeframe m5 --instruments EUR-USD --demo --test-mode"
    )
    
    parser.add_argument(
        '--timeframe', '-t', 
        default='H4',
        help='Trading timeframe (m1, m5, m15, H1, H4, D1)'
    )
    
    parser.add_argument(
        '--instruments', '-i',
        default='EUR-USD,GBP-USD,XAU-USD',
        help='Comma-separated list of instruments'
    )
    
    parser.add_argument(
        '--quality-threshold', '-q',
        type=float, default=8.0,
        help='Quality threshold for trading signals'
    )
    
    parser.add_argument(
        '--demo', action='store_true', default=True,
        help='Use demo account (default: True)'
    )
    
    parser.add_argument(
        '--real', action='store_true',
        help='Use real account (overrides --demo)'
    )
    
    parser.add_argument(
        '--test-mode', action='store_true',
        help='Enable test mode (simulation without real timeframe waiting)'
    )
    
    parser.add_argument(
        '--max-cycles', type=int,
        help='Maximum number of cycles to run (useful for testing)'
    )
    
    args = parser.parse_args()
    
    # Parse instruments
    instruments = [inst.strip() for inst in args.instruments.split(',')]
    
    # Determine demo mode
    demo_mode = not args.real  # Default to demo unless --real is specified
    
    # Create and run orchestrator
    orchestrator = SimpleTradingOrchestrator(
        timeframe=args.timeframe,
        instruments=instruments,
        quality_threshold=args.quality_threshold,
        demo=demo_mode,
        test_mode=args.test_mode
    )
    
    if args.test_mode or args.max_cycles:
        orchestrator.run_continuous(max_cycles=args.max_cycles)
    else:
        orchestrator.run_continuous()


if __name__ == "__main__":
    main() 