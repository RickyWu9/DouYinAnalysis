我们将使用Marsyas提供的机器学习数据集，这是一个名为GTZAN的开源软件。它是每30秒长的1000个音轨的集合。代表10种类型，每种包含100个音轨。所有音轨都是.au格式的22050Hz单声道16位音频文件。我们将使用所有提供的类型（blues, classical, jazz, country, pop, rock, metal, disco, hip-hop, reggae）。对于音乐类型分类，我们将更容易使用WAV文件，因为它们可以通过scipy库轻松读取。因此，我们必须将AU文件转换为WAV格式。

可以在此处(http://opihi.cs.uvic.ca/sound/genres.tar.gz)访问该机器学习数据集。