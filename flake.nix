{
  description = "DevOps Learning Environment with Python and DevOps tools";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      # Define the systems we want to support
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      # Helper function to generate an attribute set for each system
      forAllSystems = fn: nixpkgs.lib.genAttrs supportedSystems fn;

      # Function to create devShell for a specific system
      mkDevShell =
        system:
        let
          pkgs = import nixpkgs { inherit system; };

          python = pkgs.python313;

          # Python packages needed for development - streamlined to only include packages used in guides
          pythonEnv = python.withPackages (
            ps: with ps; [
              typer

              # Testing (essential for dev workflow)
              pytest
              pytest-cov
            ]
          );

          # DevOps tools - Streamlined for learning
          devopsTools = with pkgs; [
            # Container tools - Docker is sufficient for learning
            git
            figlet # For ASCII art
          ];

          myShell = pkgs.mkShell {
            name = "10000-dice-game-shell";
            buildInputs = [ pythonEnv ] ++ devopsTools;

            shellHook = ''
              if [ ! -d .venv ]; then
                python -m venv .venv
                echo "Created new Python virtual environment in .venv/"
              fi
              source .venv/bin/activate

              if [ -f requirements.txt ]; then
                pip install -r requirements.txt
              fi

              export PATH="$PATH:$(pwd)/.venv/bin"

              # Set up environment variables
              export KUBECONFIG="$(pwd)/infrastructure/kubernetes/kubeconfig"

              clear
              figlet "10,000 Dice Game"
              echo ""
              echo "🎲 Welcome to the GitHub-Issues-Based 10,000 Dice Game! 🎲"
              echo "🐍 Powered by Python $(python --version 2>&1 | cut -d' ' -f2) & GitHub Actions"
              echo ""
              echo "📋 Project Overview:"
              echo "   - Always-running dice game where players interact via GitHub Issues"
              echo "   - Play with simple commands: -roll, -keep, and -help"
              echo "   - Game state persists in JSON and displays on README.md"
              echo ""
              echo "🧰 Development Tools Ready:"
              echo "   - Python environment activated"
              echo "   - Git configured for GitHub interaction"
              echo "   - Testing framework available with pytest"
              echo ""
              echo "Ready to roll! Happy coding! 🎮 🎲 🎯"
              echo ""
            '';
          };
        in
        myShell;
    in
    {
      # Create devShells for all supported systems
      devShells = forAllSystems (system: {
        default = mkDevShell system;
      });

      # For compatibility with 'nix develop'
      devShell = forAllSystems (system: mkDevShell system);
    };
}
