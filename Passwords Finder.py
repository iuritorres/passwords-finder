import subprocess
import tkinter as tk


def format_data(data: dict) -> str:
	return ''.join([f'{data[0]:20}: {data[-1]}\n' for data in data.items()])


def get_data_from_line(line: str) -> str:
	return line.split(':')[-1].strip()


def get_profiles() -> list[str]:
	profiles = []
	command_output = subprocess.check_output(
		'netsh wlan show profiles',
		encoding='cp858',
		creationflags=subprocess.CREATE_NO_WINDOW
	)
	output_lines = reversed([line for line in command_output.split('\n') if line != ''])

	for line in output_lines:
		if line.startswith('---'): break

		profiles.append(get_data_from_line(line))

	return profiles


def get_profile_password(profile: str) -> str:
	try:
		command_output = subprocess.check_output(
			f'netsh wlan show profile "{profile}" key=clear',
			encoding='cp858',
			creationflags=subprocess.CREATE_NO_WINDOW
		)
		output_lines = [line.strip() for line in command_output.split('\n') if line != '']

		for line in output_lines:
			if (line.__contains__('Conteúdo da Chave')):
				return get_data_from_line(line)

	except subprocess.CalledProcessError as error:
		return error


def show_alert(title: str, text: str) -> None:
	screen = tk.Tk()

	screen.title(title)
	label = tk.Label(
		screen,
		text=text,
		justify='left',
		font=('Consolas', 12)
	)
	label.pack(padx=10, pady=10)
	
	screen.eval('tk::PlaceWindow . center')
	screen.mainloop()


if __name__ == '__main__':
	data = {}
	alert_text = 'Não há nenhuma senha salva no seu computador.'

	for profile in get_profiles():
		password = get_profile_password(profile)

		if password.__class__ == subprocess.CalledProcessError:
			data[profile] = "Não encontrada"
			continue

		data[profile] = password

	show_alert('Senhas Salvas', format_data(data) if any(data) else alert_text)
