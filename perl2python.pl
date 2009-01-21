use Getopt::Long;

my $input = ".";
my $output = ".";

$result = GetOptions("input=s" => \$input,
		     "output=s" => \$output);

sub python_escape {
	my $x = shift;

	return '' unless defined($x);

	$x =~ s/\\/\\\\/gs;
	$x =~ s/'/\\'/gs;
	$x =~ s/([\x00-\x1f])/sprintf("\\x%02x", ord($1))/ges;

	return $x;
}

# print "$input\n";

push(@INC, $input);

my $n;
for($n = 0; $n < 256; $n++) {

	eval( sprintf("require x%02x;\n", $n) );

	next unless( $#{$Text::Unidecode::Char[$n]} >= 0 );

	# print "$n\n";

	open(PYTHON, sprintf(">%s/x%02x.py", $output, $n));
	print PYTHON "data = (\n";

	my $m = 0;
	for my $t (@{$Text::Unidecode::Char[$n]}) {
		print PYTHON "'", &python_escape($t), "',    # ";
		printf PYTHON "0x%02x\n", $m;
		$m++;
	}

	print PYTHON ")\n";
	close(PYTHON)
}
