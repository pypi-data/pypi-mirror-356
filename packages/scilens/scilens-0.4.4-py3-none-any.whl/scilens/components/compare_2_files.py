import os,re
from scilens.run.task_context import TaskContext
from scilens.readers.reader_interface import ReaderInterface
from scilens.components.file_reader import FileReader
from scilens.components.compare_models import SEVERITY_ERROR,SEVERITY_WARNING
from scilens.components.compare_errors import CompareErrors
from scilens.components.compare_floats import CompareFloats
class Compare2Files:
	def __init__(A,context):A.context=context
	def compare(B,path_test,path_ref):
		h='status';g='severity';f='comparison_errors';e='comparison';Y=path_ref;X=path_test;W='err_index';V='reader';U='skipped';T=None;R='metrics';Q='error';P=True;O='ref';J='path';I='test';A={I:{},O:{},e:T,f:T};H={I:{J:X},O:{J:Y}};S=B.context.config.compare.sources.not_matching_source_ignore_pattern
		for(C,K)in H.items():
			if not K.get(J)or not os.path.exists(K[J]):
				if S:
					if S=='*':A[U]=P;return A
					else:
						i=os.path.basename(Y if C==I else X);j=re.search(S,i)
						if j:A[U]=P;return A
				A[Q]=f"file {C} does not exist";return A
		k=FileReader(B.context.working_dir,B.context.config.file_reader,B.context.config.readers,config_alternate_path=B.context.origin_working_dir)
		for(C,K)in H.items():H[C][V]=k.read(K[J])
		D=H[I][V];F=H[O][V]
		if not D or not F:A[U]=P;return A
		A[I]=D.info();A[O]=F.info()
		if D.read_error:A[Q]=D.read_error;return A
		E=CompareErrors(B.context.config.compare.errors_limit,B.context.config.compare.ignore_warnings);Z=CompareFloats(E,B.context.config.compare.float_thresholds);D.compare(Z,F,param_is_ref=P);G=E.root_group;L=T
		if B.context.config.compare.metrics_compare and(D.metrics or F.metrics):
			n,L=E.add_group(R,R,parent=G)
			if B.context.config.compare.metrics_thresholds:a=CompareFloats(E,B.context.config.compare.metrics_thresholds)
			else:a=Z
			a.compare_dicts(D.metrics,F.metrics,L)
		M={'total_diffs':G.total_diffs}
		if G.info:M.update(G.info)
		if L:
			N={}
			for b in[SEVERITY_ERROR,SEVERITY_WARNING]:
				for(l,c)in enumerate(E.errors[b]):
					if c.group==L.id:N[c.info['key']]={g:b,W:l}
			M[R]={}
			for C in D.metrics.keys():M[R][C]={h:N[C][g],W:N[C][W]}if C in N else{h:'success'}
		A[e]=M;A[f]=E.get_data()
		if G.error:A[Q]=G.error;return A
		D.close();F.close();d=len(E.errors[SEVERITY_ERROR])
		if d>0:m=f"{d} comparison errors";A[Q]=m
		return A