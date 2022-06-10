#!/bin/bash

which python3 > /dev/null
if [ "$?" == "0" ]; then
	echo "python3 est déja installé"
else
	echo "python3 n'est pas installé."
	read -p "Procéder à l'installation ? (y/n) " yn

	case $yn in 
		y ) echo "sudo apt install python3 -y";
			sudo apt install python3 -y;;
		n ) echo "Annulation de l'installation";
			exit 1;;
		* ) echo "Réponse invalide, arrêt";
			exit 1;;
	esac
fi

which pip3 > /dev/null
if [ "$?" == "0" ]; then
	echo "pip3 est déja installé"
else
	echo "pip3 n'est pas installé."
	read -p "Procéder à l'installation ? (y/n) " yn

	case $yn in 
		y ) echo "sudo apt install python3-pip -y";
			sudo apt install python3-pip -y;;
		n ) echo "Annulation de l'installation";
			exit 1;;
		* ) echo "Réponse invalide, arrêt";
			exit 1;;
	esac
fi

echo "Installation des librairies nécessaires..."
pip3 install -r requirements.txt
echo "Installation terminée"