
package com.djs.learn.junit;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({NormalTest.class, ParameterizedTest.class})
public class TestMain
{}
