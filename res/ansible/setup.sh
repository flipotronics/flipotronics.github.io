export ANSIBLE_HOSTS=/Users/mat/flipotronics.github.io/res/ansible/hosts

echo "flipotronics install synth A1"
echo -n Password of your Raspberry PI [raspberry]: 
read -s PWD
PWD=${PWD:-raspberry}
echo
echo "starting install"

ansible-playbook -i $ANSIBLE_HOSTS --extra-vars "ansible_user=pi ansible_password=$PWD" raspi.yaml

ansible-playbook -i $ANSIBLE_HOSTS  user.yaml

#ansible-playbook -i $ANSIBLE_HOSTS --extra-vars "ansible_user=pi ansible_password=$PWD" os.yaml

#ansible-playbook -i $ANSIBLE_HOSTS --extra-vars "ansible_user=pi ansible_password=$PWD" packages.yaml

#ansible-playbook -i $ANSIBLE_HOSTS --extra-vars "ansible_user=pi ansible_password=$PWD" python3.yaml




