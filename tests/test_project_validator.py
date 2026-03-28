from ai_engine.validator.project_validator import ProjectValidator


def test_project_validator():

    project_path = "generated_projects/generated_project"

    validator = ProjectValidator(project_path)

    result = validator.validate()

    print("\n--- PROJECT VALIDATION RESULT ---\n")
    print(result)


if __name__ == "__main__":
    test_project_validator()