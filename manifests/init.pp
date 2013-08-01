class test {

	file { '/home/vagrant/readme.txt':
		ensure => present,
		content => "Sylvan is evil. Hello, World! Test complete. -Robot Aaron",
	}
}	

include test
