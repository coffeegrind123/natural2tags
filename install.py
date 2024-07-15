import launch

if not launch.is_installed("text2tags-lib"):
    print("Installing requirements for Prompt Formatter")
    launch.run_pip("install text2tags-lib", "make it so we can do this")
