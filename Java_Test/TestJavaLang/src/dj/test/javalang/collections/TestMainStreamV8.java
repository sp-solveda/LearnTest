
package dj.test.javalang.collections;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class TestMainStreamV8
{
	public void testSample1(){
		List<Integer> list = Arrays.asList(8, 18, 28, 38);

		list.stream().filter(item -> item > 20).forEach(item -> System.out.println(item));
		list.parallelStream().filter(item -> item < 20).forEach(item -> System.out.println(item));
	}

	public void testCreate(){
		Stream<String> empty = Stream.empty();
		Stream<Integer> singleElement = Stream.of(1);
		Stream<Integer> fromArray = Stream.of(1, 2, 3);

		System.out.println("empty = " + empty);
		System.out.println("singleElement = " + singleElement);
		System.out.println("fromArray = " + fromArray);
	}

	public void testTerminalOperations(){
		// Cannot reuse stream, as these methods are terminal operations.
		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			System.out.println("Stream.count() = " + s.count());
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			Optional<String> min = s.min((s1, s2) -> s1.length() - s2.length());
			min.ifPresent(System.out::println);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			Optional<String> max = s.max((s1, s2) -> s1.length() - s2.length());
			max.ifPresent(System.out::println);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			Optional<String> findAny = s.findAny();
			findAny.ifPresent(System.out::println);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			Optional<String> findFirst = s.findFirst();
			findFirst.ifPresent(System.out::println);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			Optional<String> findFirst = s.findFirst();
			findFirst.ifPresent(System.out::println);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			System.out.println("Stream.allMatch() = " + s.allMatch(x -> x.length() == 6));
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			System.out.println("Stream.anyMatch() = " + s.anyMatch(x -> x.length() == 6));
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			System.out.println("Stream.noneMatch() = " + s.noneMatch(x -> x.length() == 6));
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			s.forEach(System.out::print);
			System.out.println();
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			String result = s.reduce("Start", (s1, s2) -> s1 = s1 + "-" + s2);
			System.out.println("Stream.reduce() = " + result);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			String result = s.reduce("Line", String::concat);
			System.out.println("Stream.reduce() = " + result);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			TreeSet<String> collect = s.collect(TreeSet::new, TreeSet::add, TreeSet::addAll);
			System.out.println("Stream.collect() = " + collect);
		}

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			StringBuilder collect = s.collect(StringBuilder::new, StringBuilder::append, StringBuilder::append);
			System.out.println("Stream.collect() = " + collect);
		}
	}

	public void testIntermediateOperations(){
		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.filter(x -> x.length() > 6).forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.distinct().forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.skip(2).forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.limit(2).forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			// Map is similar to covert something.
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.map(x -> x.length()).forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			{
				Stream<List<String>> s = Stream.of(Arrays.asList("monkey", "gorilla"), Arrays.asList("bonobo"), Arrays.asList("monkey", "gorilla"));
				s.forEach(System.out::println);
			}

			{
				Stream<List<String>> s = Stream.of(Arrays.asList("monkey", "gorilla"), Arrays.asList("bonobo"), Arrays.asList("monkey", "gorilla"));
				s.flatMap(x -> x.stream()).forEach(System.out::println);
			}
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.sorted().forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.sorted(Comparator.reverseOrder()).forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			s.peek(x -> System.out.print(x + "-")).forEach(x -> System.out.println(x.length()));
		}
	}

	public void testGenerate(){
		{
			Stream<Double> s = Stream.generate(Math::random);
			s.limit(5).forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			Stream<Double> odd = Stream.iterate(1.0, x -> x / 2);
			odd.limit(5).forEach(System.out::println);
		}

		System.out.println("--------------------");

		{
			Stream<Integer> odd = Stream.iterate(1, x -> x + 2);
			odd.limit(5).forEach(System.out::println);
		}
	}

	public void testCollectors1(){
		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			System.out.println("Stream.collect(Collectors.joining()) = " + s.collect(Collectors.joining()));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			System.out.println("Stream.collect(Collectors.joining()) = " + s.collect(Collectors.joining(",")));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			System.out.println("Stream.collect(Collectors.toCollection()) = " + s.collect(Collectors.toCollection(TreeSet::new)));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo");
			System.out.println("Stream.collect(Collectors.toMap()) = " + s.collect(Collectors.toMap(x -> x, String::length)));
		}
	}

	public void testCollectors2(){
		{
			Stream<String> s = Stream.empty();
			System.out.println("Stream.collect(Collectors.groupingBy(Map/List)) = " + s.collect(Collectors.groupingBy(String::length)));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			System.out.println("Stream.collect(Collectors.groupingBy(Map/List)) = " + s.collect(Collectors.groupingBy(String::length)));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			System.out.println("Stream.collect(Collectors.groupingBy(Map/Set)) = " + s.collect(Collectors.groupingBy(String::length, Collectors.toSet())));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			System.out.println("Stream.collect(Collectors.groupingBy(TreeMap/List)) = "
			        + s.collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.toList())));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			System.out.println("Stream.collect(Collectors.groupingBy(TreeMap/Set)) = "
			        + s.collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.toSet())));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.empty();
			System.out.println("Stream.collect(Collectors.partitioningBy(List)) = " + s.collect(Collectors.partitioningBy(x -> x.length() > 6)));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			System.out.println("Stream.collect(Collectors.partitioningBy(List)) = " + s.collect(Collectors.partitioningBy(x -> x.length() > 6)));
		}

		System.out.println("--------------------");

		{
			Stream<String> s = Stream.of("monkey", "gorilla", "bonobo", "monkey", "gorilla");
			System.out.println("Stream.collect(Collectors.partitioningBy(Set)) = "
			        + s.collect(Collectors.partitioningBy(x -> x.length() > 6, Collectors.toSet())));
		}
	}

	public static void main(String[] args){
		TestMainStreamV8 testMain = new TestMainStreamV8();

		testMain.testSample1();
		System.out.println("============================================================");

		testMain.testCreate();
		System.out.println("============================================================");

		testMain.testTerminalOperations();
		System.out.println("============================================================");

		testMain.testIntermediateOperations();
		System.out.println("============================================================");

		testMain.testGenerate();
		System.out.println("============================================================");

		testMain.testCollectors1();
		System.out.println("============================================================");

		testMain.testCollectors2();
		System.out.println("============================================================");
	}
}
