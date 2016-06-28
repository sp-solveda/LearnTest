
package com.djs.test.spring_sample.knightI;

import com.djs.test.spring_sample.knight.QuestFailedException;

public interface Knight
{
	public String getName();

	public Object embarkOnQuest() throws QuestFailedException;
}
