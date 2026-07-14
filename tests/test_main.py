from mini_projeto.main import main


def test_main_runs_without_error(capsys):
    main()
    captured = capsys.readouterr()
    assert "Projeto base Python" in captured.out
