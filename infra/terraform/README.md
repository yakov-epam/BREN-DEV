# Comprehensive guide to Terraforming

> Many developers are scared of terraform, it shouldn't be this way. Let them be scared of yaml instead.

1. Install Terraform.
2. Optional: Add an alias to your rc/profile file `alias tf="terraform"` and restart the terminal session.
3. Run `tf init`.
4. Run `tf fmt`.
5. Copy `config.example.yaml` to `config.yaml` and adjust it as needed.
6. Run `tf plan --out=plan.txt` and check the output carefully before proceeding further.
7. Run `tf apply plan.txt`.
