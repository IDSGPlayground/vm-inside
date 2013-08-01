class test {

	file { '/home/vagrant/readme.txt':
		ensure => present,
		content => "Sylvan is evil, and so am I, apparently. Hello, World! Test complete. -Robot Aaron",
	}
}	

include test
