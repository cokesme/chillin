#!/bin/bash
# various stack overflows etc.
function mirror {
	if [ -z $(which git) ]; then
		echo "need to install git"
	fi

	if [ -z "${GITHUB_TOKEN}" ]; then
		echo "set github token" 
	fi

	# https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository
	git clone --bare github:/$1/$2.git

	cd $2.git;

	new_repo="$2-mirror"

	# create the repo
	curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user/repos -d '{"name": "'"$new_repo"'"}'

	# push the mirror
	git push --mirror github:/cokesme/$new_repo.git

	cd .. && rm -rf $2.git;
}

# if this isn't sourced just run it 
if [ $# -eq 2 ]; then 
	mirror $1 $2
fi
